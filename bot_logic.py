import json
from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup


# Фильтр, проверяющий доступ юзера
class Access(BaseFilter):
    def __init__(self, access: list[str]) -> None:
        # В качестве параметра фильтр принимает список со строками
        self.access = access

    async def __call__(self, message: Message) -> bool:
        user_id_str = str(message.from_user.id)
        return user_id_str in self.access


# Состояния FSM
class FSM(StatesGroup):
    # Создаем экземпляры класса State, последовательно перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с юзером
    policy = State()            # Состояние ожидания соглашения с policy
    platform_user_id = State()  # Состояние ожидания ввода id
    upload_photo = State()      # Состояние ожидания загрузки фото
    upload_2_photo = State()    # Состояние ожидания загрузки ДВУХ фото


# Запись данных item в указанный json file по ключу key
def log(file, key, item):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    data.setdefault(key, []).append(item)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# #  Палит админу действия юзеров
# async def intel(bot, message, admins, silence: bool):
#     user = str(message.from_user.id)
#     if user not in admins:
#         for i in admins:
#             await bot.send_message(text=f'{message.text} id{user} {message.from_user.full_name}'
#                                         f' @{message.from_user.username}', chat_id=i, disable_notification=silence)
# не работает

