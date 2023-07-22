import time
import requests
import os
import json
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from datetime import datetime
from bot_logic import log, Access
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy
from variables import admins, SAVE_DIR, book, SAMPLE


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token


# @router.message()
# async def blabla(message: Message):
#     await message.answer(text='ok')
#     # for i in message:
#     #     if not str(i).endswith('None)'):
#     #         print(i)
#
#     print(message.reply_to_message.message_id)



# чекнуть не в бане ли юзер
@router.message(Access(book['ban']))
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
    log('logs.json', user, 'privacy_ok')
    # await callback.answer(text='Thanks! Please now send your selfie.')
    await bot.send_message(text='Thanks! Please now see the examples and send your selfie.', chat_id=user)
    # time.sleep(1)

    await bot.send_photo(photo='https://i.ibb.co/z89YvcS/collage.jpg', caption='Examples', chat_id=user)

    # Loop through the list of photo filenames and add them to the media_group list


# /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    user = str(message.from_user.id)
    log('logs.json', user, '/help')
    await message.answer('If something does not work, contact @its_dmitrii')


# user sent photo
@router.message(F.content_type.in_({'photo', 'document'}))
async def save_photo(m: types.Message, bot:Bot):
    user = m.from_user
    log('logs.json', m.from_user.id, 'SENT_PHOTO')

    # for i in m:
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

        # записи
        log('logs.json', m.from_user.id, 'SENT_PHOTO')
        log('user_baza.json', 'selfie_done', str(user.id))
        book.setdefault('selfie_done', []).append(str(user.id))

        # Отправить файл админу и ожидать приемки
        for i in admins:
            await bot.forward_message(chat_id=i, from_chat_id=user.id, message_id=m.message_id)
            await bot.send_message(chat_id=i, text=f'Принять файл от @{user.username} id{user.id}?',
                                   reply_markup=keyboard_admin)

    else:
        await m.reply("Failed to save the photo.")

    print(msg_time)
    print(m.from_user.full_name, 'sent photo')
    print()



