import json
from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup
import requests
import os
from settings import SAVE_DIR


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
    # Состояния, в которых будет находиться бот в разные моменты взаимодействия с юзером
    policy = State()            # Состояние ожидания соглашения с policy
    platform_user_id = State()  # Состояние ожидания ввода id
    upload_photo = State()      # Состояние ожидания загрузки фото
    upload_2_photo = State()    # Состояние ожидания загрузки ДВУХ фото
    waiting_verif = State()     # Юзер всё скинул и ждет код


# Запись данных item в указанный json file по ключу key
def log(file, key, item):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    data.setdefault(str(key), []).append(item)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# скачать в SAVE_DIR
async def dwnld_photo_or_doc(msg, bot, worker, tkn):
    # получение url файла
    if msg.document:
        file_id = msg.document.file_id
    else:
        file_id = msg.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path

    # скачивание файла
    msg_time = str(msg.date.date())+'_'+str(msg.date.time()).replace(':', '-')
    tg_file_link = f'https://api.telegram.org/file/bot{tkn}/{file_url}'
    response = requests.get(tg_file_link)
    file_path = os.path.join(SAVE_DIR, f'{msg_time}_id{str(worker.id)}_{file_info.file_path.split("/")[-1]}')
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print('file ok')
    # return tg_file_link
