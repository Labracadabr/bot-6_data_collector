import time
import requests
import os
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
# from lexic.lexic import RU
from datetime import datetime
from bot_logic import log, Access
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy


# Инициализация всяких штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
verification_code: str = '125'
admins: list[str] = ["992863889"]
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot_collector\SELFIES"
bans = []


@router.message(Access(bans))
async def no_access(message: Message):
    await message.answer(text='You are banned by @its_dmitrii')
    await message.answer(text=f'id {message.from_user.id}')


# /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot):
    m = message.from_user
    user = str(m.id)
    msg_time = datetime.now().strftime("%d/%m/%Y %H:%M")

    log('logs.json', 'logs', f'{msg_time}, {m.full_name}, @{m.username}, id {user}, {m.language_code}')
    log('logs.json', user, '/start')

    await message.answer(text='Hi!\nPlease read our privacy policy by the button below '
                              'and press ✅ button to continue.', reply_markup=keyboard_privacy)
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if user not in admins:
        for i in admins:
            await bot.send_message(text=f'{message.text} id{user} {message.from_user.full_name}'
                                        f' @{message.from_user.username}', chat_id=i, disable_notification=True)


# privacy ✅
@router.callback_query(Text(text=['ok_pressed']))
async def privacy_ok(callback: CallbackQuery, bot:Bot):
    user = str(callback.from_user.id)
    # await callback.answer(text='Thanks! Please now send your selfie.')
    await bot.send_message(text='Thanks! Please now see the examples and send your selfie.', chat_id=user)
    # time.sleep(1)
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
    user = m.from_user
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
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path

    response = requests.get(f'https://api.telegram.org/file/bot{TKN}/{file_url}')
    if response.status_code == 200:
        file_path = os.path.join(SAVE_DIR, f'{msg_time}_id{str(user.id)}_{file_info.file_path.split("/")[-1]}')
        print(file_path)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        await m.reply(f"Thanks! Please wait for us to check your work.")

        # Отправить файл админу и ожидать приемки
        for i in admins:
            await bot.forward_message(chat_id=i, from_chat_id=user.id, message_id=m.message_id)
            await bot.send_message(chat_id=i, text=f'Принять файл от @{user.username} id {user.id}?',
                                   reply_markup=keyboard_admin)
    else:
        await m.reply("Failed to save the photo.")

    print(str(m.date.date())+'_'+str(m.date.time()))
    print(m.from_user.full_name, 'sent photo')
    print()


# admin ✅
@router.callback_query(Text(text=['admin_ok']))
async def admin_ok(callback: CallbackQuery, bot:Bot):
    user = str(callback.message.text).split()[-1][:-1]
    print(user)

    await bot.send_message(chat_id=user, text=f"Success! Here is your verification code:")
    await bot.send_message(chat_id=user, text=f'<code>{verification_code}</code>', parse_mode='HTML')


# admin ❌
@router.callback_query(Text(text=['admin_no']))
async def admin_no(callback: CallbackQuery, bot: Bot):
    user = str(callback.message.text).split()[-1][:-1]
    await bot.send_message(chat_id=user, text="Wrong, please retry")

