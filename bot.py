import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers, selfie_user_handlers, med_user_handlers
from settings import project


# нужный проект выберется автоматически на основе project из settings
projects = {'selfie': selfie_user_handlers.router,
            'med': med_user_handlers.router,
            }


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрируем роутеры в диспетчере
    dp.include_router(projects[project])
    dp.include_router(admin_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)  # False > бот ответит на сообщения, присланные за время спячки
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())