import time
import requests
import os
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import KeyboardButton, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from lexic.lexic import LEXICON_RU
from datetime import datetime
from bot_logic import log, book
from config_data.config import Config, load_config


# Инициализация всяких штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
verification_code: str = '125'
admins: list = ["992863889"]
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot_collector\SELFIES"
privacy_en: str = "https://drive.google.com/file/d/1RddAFv77L6sL2tvPJBFxA5eI-Zb9Z1AC/view"

# кнопки как доп опция ответа
button_start: KeyboardButton = KeyboardButton(text='/start')
button_help: KeyboardButton = KeyboardButton(text='/help')
button_ok: KeyboardButton = KeyboardButton(text='✅')
button_no: KeyboardButton = KeyboardButton(text='❌')
url_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Privacy policy',
    url=privacy_en)
ok_button: InlineKeyboardButton = InlineKeyboardButton(
    text='✅',
    callback_data='ok_pressed')

# клавиатуры из таких кнопок
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[url_button]])
keyboard_ok: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[ok_button]])


# /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot):
    m = message.from_user
    user = str(m.id)
    msg_time = datetime.now().strftime("%d/%m/%Y %H:%M")

    log('logs.json', 'logs', f'{msg_time}, {m.full_name}, @{m.username}, id {user}, {m.language_code}')
    log('logs.json', user, '/start')

    await message.answer(text='Hi!\nPlease read our privacy policy by the button below '
                              'and press ✅ button to continue.', reply_markup=keyboard)
    time.sleep(1)
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if user not in admins:
        for i in admins:
            await bot.send_message(text=f'{message.text} id{user} {message.from_user.full_name}'
                                        f' @{message.from_user.username}', chat_id=i, disable_notification=True)

    # book.setdefault(user, {'used': [], 'bot_word': '', 'player_word': '', 'help_word': 'й', 'mode': 'Hard'})
    print(book)


# ✅
@router.callback_query(Text(text=['ok_pressed']))
async def process_buttons_press(callback: CallbackQuery, bot:Bot):
    user = str(callback.from_user.id)
    # await callback.answer(text='Thanks! Please now send your selfie.')
    await bot.send_message(text='Thanks! Please now see the examples and send your selfie.', chat_id=user)
    time.sleep(1)
    await bot.send_message(text='🖼(тут будут примеры)', chat_id=user)


# /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', user, '/help')
    await message.answer('no help')


# user sent photo
@router.message(F.content_type.in_({'photo', 'document'}))
async def save_photo(m: types.Message, bot:Bot):
    log('logs.json', m.from_user.id, 'SENT_PHOTO')
    # await m.answer('Processing...')

    # for i in str(m).split():
    #     print(i)
    print()
    msg_time = str(m.date.date())+'_'+str(m.date.time()).replace(':', '-')

    # save the photo locally
    if m.document:
        file_id = m.document.file_id
    else:
        file_id = m.photo[-1].file_id

    print(file_id)
    file_info = await bot.get_file(file_id)
    print(file_info)
    file_url = file_info.file_path
    print(file_url)

    response = requests.get(f'https://api.telegram.org/file/bot{TKN}/{file_url}')
    if response.status_code == 200:
        file_path = os.path.join(SAVE_DIR, f'{msg_time}_id{str(m.from_user.id)}_{file_info.file_path.split("/")[-1]}')
        with open(file_path, 'wb') as f:
            f.write(response.content)
        await m.reply(f"Success! Here is your verification code:")
        await m.answer(f'<code>{verification_code}</code>', parse_mode='HTML')
    else:
        await m.reply("Failed to save the photo.")

    print(str(m.date.date())+'_'+str(m.date.time()))
    print(m.from_user.full_name, 'sent photo')
    print()

# https://api.telegram.org/bot6316389480:AAGr-cfLXP0gE2L2QUDCA9JAFjkj-3IgQi4/getFile?file_id=AgACAgUAAxkBAAMQZLkzuebs37Tl53lXghOyQ3YJx24AArS3MRuKJchV_lzY0AW56uABAAMCAANtAAMvBA
# https://api.telegram.org/bot6316389480:AAGr-cfLXP0gE2L2QUDCA9JAFjkj-3IgQi4/photos/file_0.jpg

