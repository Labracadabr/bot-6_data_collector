import time
import requests
import os
import json
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from bot_logic import log, Access
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy
from variables import admins, SAVE_DIR, book, SAMPLE
from lexic.lexic import EN


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    log('logs.json', str(message.from_user.id), '/help')
    await message.answer(EN['help'])


# чекнуть не в бане ли юзер
@router.message(Access(book['ban']))
async def no_access(message: Message):
    await message.answer(EN['ban'])


# команда /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot):
    worker = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")

    # ведение учета
    log('logs.json', 'logs', f'{msg_time}, {worker.full_name}, @{worker.username}, id {worker.id}, {worker.language_code}')
    log('logs.json', worker.id, '/start')

    # приветствие и выдача
    await message.answer(text=EN['start'], reply_markup=keyboard_privacy)
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if str(worker.id) not in admins:
        for i in admins:
            await bot.send_message(text=f'Bot started by id{worker.id} {worker.full_name} @{worker.username}', chat_id=i, disable_notification=True)


# согласен с политикой ✅
@router.callback_query(Text(text=['ok_pressed']))
async def privacy_ok(callback: CallbackQuery, bot:Bot):
    worker = callback.from_user

    # ведение учета
    if str(worker.id) not in admins:
        log('logs.json', worker, 'privacy_ok')

    # выдать инструкцию и примеры
    await bot.send_message(text=EN['instruct1'], chat_id=worker.id)
    await bot.send_photo(photo=SAMPLE, caption='Examples', chat_id=worker.id)
    await bot.send_message(text=EN['instruct2'], chat_id=worker.id)
    time.sleep(3)
    await bot.send_message(text=EN['instruct3'], chat_id=worker.id)


# юзер отправил фото или документ
@router.message(F.content_type.in_({'photo', 'document'}))
async def save_photo(m: types.Message, bot:Bot):
    worker = m.from_user
    msg_time = str(m.date.date())+'_'+str(m.date.time()).replace(':', '-')

    # получение url файла
    if m.document:
        file_id = m.document.file_id
    else:
        file_id = m.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path

    # скачивание файла
    response = requests.get(f'https://api.telegram.org/file/bot{TKN}/{file_url}')
    file_path = os.path.join(SAVE_DIR, f'{msg_time}_id{str(worker.id)}_{file_info.file_path.split("/")[-1]}')
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    await m.reply(f"Thanks! Please wait for us to check your work.")

    # ведение учета
    if str(worker.id) not in admins:
        log('logs.json', worker.id, 'SENT_PHOTO')
        log('user_baza.json', 'selfie_done', str(worker.id))
        book.setdefault('selfie_done', []).append(str(worker.id))

    # Отправить файл админу и ожидать приемки
    for i in admins:
        await bot.forward_message(chat_id=i, from_chat_id=worker.id, message_id=m.message_id)
        await bot.send_message(chat_id=i, text=f'Принять файл от {worker.full_name} @{worker.username} id{worker.id}?',
                               reply_markup=keyboard_admin)

    print(msg_time)
    print(worker.full_name, 'sent photo')
    print()



