import asyncio
# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers, user_handlers


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)  # False > бот ответит на сообщения, присланные за время спячки
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())