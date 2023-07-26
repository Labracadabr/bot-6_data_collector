import time
import requests
import os
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from bot_logic import log, Access
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy
from settings import admins, SAVE_DIR, book, project
from lexic.lexic import EN


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    log('logs.json', str(message.from_user.id), '/help')
    await message.answer(EN[project]['help'])


# чекнуть не в бане ли юзер
@router.message(Access(book['ban']))
async def no_access(message: Message):
    await message.answer(EN[project]['ban'])


# команда /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot):
    worker = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")

    # логи
    log('logs.json', 'logs',
        f'{msg_time}, {worker.full_name}, @{worker.username}, id {worker.id}, {worker.language_code}')
    log('logs.json', worker.id, '/start')

    # приветствие и выдача политики
    await message.answer(text=EN[project]['start'], reply_markup=keyboard_privacy)
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if str(worker.id) not in admins:
        for i in admins:
            await bot.send_message(text=f'Bot started by id{worker.id} {worker.full_name} @{worker.username}',
                                   chat_id=i, disable_notification=True)


# согласен с политикой ✅
@router.callback_query(Text(text=['ok_pressed']))
async def privacy_ok(callback: CallbackQuery, bot: Bot):
    worker = callback.from_user

    # логи
    if str(worker.id) not in admins:
        log('logs.json', worker.id, 'privacy_ok')

    # выдать инструкцию и примеры
    await bot.send_message(text=EN[project]['instruct1'], chat_id=worker.id)
    await bot.send_photo(photo=EN[project]['example_link'], caption='Examples', chat_id=worker.id)
    await bot.send_message(text=EN[project]['instruct2'], chat_id=worker.id, parse_mode='HTML')
    time.sleep(3)
    await bot.send_message(text=EN[project]['instruct3'], chat_id=worker.id)


# юзер отправил фото или документ
@router.message(F.content_type.in_({'photo', 'document'}))
async def save_photo(msg: Message, bot: Bot):
    worker = msg.from_user
    msg_time = str(msg.date.date())+'_'+str(msg.date.time()).replace(':', '-')

    # получение url файла
    if msg.document:
        file_id = msg.document.file_id
    else:
        file_id = msg.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path

    # скачивание файла
    response = requests.get(f'https://api.telegram.org/file/bot{TKN}/{file_url}')
    file_path = os.path.join(SAVE_DIR, f'{msg_time}_id{str(worker.id)}_{file_info.file_path.split("/")[-1]}')
    with open(file_path, 'wb') as f:
        f.write(response.content)
    await msg.reply(f"Thanks! Please wait for us to check your work.")

    # логи
    if str(worker.id) not in admins:
        log('logs.json', worker.id, 'SENT_FILE')
        log('user_baza.json', EN[project]['log'], str(worker.id))
        book.setdefault(EN[project]['log'], []).append(str(worker.id))

    # Отправить файл админу для вынесения вердикта
    for i in admins:
        await bot.forward_message(chat_id=i, from_chat_id=worker.id, message_id=msg.message_id)
        await bot.send_message(chat_id=i, text=f'Принять файл от {worker.full_name} @{worker.username} id{worker.id}?',
                               reply_markup=keyboard_admin)

    print(msg_time)
    print(worker.full_name, 'sent file')
    print()

