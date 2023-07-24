import time
import json
import requests
import os
from aiogram import Router, Bot, F, types, Dispatcher
from aiogram.filters import Command, Text, StateFilter
# from aiogram.types import Message, CallbackQuery
from bot_logic import log, Access, FSM, dwnld_photo_or_doc
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy
from variables import admins, SAVE_DIR, book, project
from lexic.lexic import EN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, PhotoSize)


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()
user_files: [str, str] = {}


# # ww
# @router.message()
# async def prosto(message: Message):
#     print()
#     print(message.media_group_id)
#     for i in message:
#         if not str(i).endswith('None)'):
#             print(i)
# @router.message(lambda msg: msg.text == 'q')
# async def prosto(message: Message, state: FSMContext):
#     print(state)


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    log('logs.json', message.from_user.id, '/help')
    await message.answer(EN[project]['help'])


# чекнуть не в бане ли юзер
@router.message(Access(book['ban']))
async def no_access(message: Message):
    await message.answer(EN[project]['ban'])


# команда /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot, state: FSMContext):
    worker = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")

    # логи
    log('logs.json', 'logs',
        f'{msg_time}, {worker.full_name}, @{worker.username}, id {worker.id}, {worker.language_code}')
    log('logs.json', worker.id, '/start')

    # бот переходит в состояние ожидания согласие с политикой
    await state.set_state(FSM.policy)

    # приветствие и выдача политики
    await message.answer(text=EN[project]['start'], reply_markup=keyboard_privacy)
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if str(worker.id) not in admins:
        for i in admins:
            await bot.send_message(text=f'Bot started by id{worker.id} {worker.full_name} @{worker.username}',
                                   chat_id=i, disable_notification=True)


# согласен с политикой ✅
@router.callback_query(Text(text=['ok_pressed']), StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    worker = callback.from_user

    # логи
    if str(worker.id) not in admins:
        log('logs.json', worker.id, 'privacy_ok')

    # бот переходит в состояние ожидания первой фотки
    await state.set_state(FSM.upload_photo)

    # выдать инструкцию и примеры
    await bot.send_message(text=EN[project]['instruct1'], chat_id=worker.id)
    await bot.send_photo(photo=EN[project]['example_link'], caption='Examples', chat_id=worker.id)
    await bot.send_message(text=EN[project]['instruct2'], chat_id=worker.id, parse_mode='HTML')
    time.sleep(3)
    await bot.send_message(text=EN[project]['instruct3'], chat_id=worker.id)


# юзер отправил альбом - не принимается
@router.message(lambda msg: msg.media_group_id)
async def alb(msg: Message):
    worker = msg.from_user
    log('logs.json', worker.id, 'album')
    await msg.reply("Please send each file in two separate messages, not as one album.")


# юзер отправил 1ое фото
@router.message(F.content_type.in_({'photo', 'document'}), StateFilter(FSM.upload_photo))
async def photo1(msg: Message, bot: Bot, state: FSMContext):
    worker = msg.from_user

    path = await dwnld_photo_or_doc(msg, bot, worker, TKN)
    print(path)
    # сохранить первый файл
    user_files[worker.id] = []
    user_files[worker.id].append(msg.message_id)

    log('logs.json', worker.id, 'SENT_FILE_1')

    # бот переходит в состояние ожидания 2го фото
    await state.set_state(FSM.upload_2_photo)

    await msg.reply("Good, now send the second one.")


# юзер отправил 2ое фото
@router.message(F.content_type.in_({'photo', 'document'}), StateFilter(FSM.upload_2_photo))
# @router.message(lambda msg: msg.text == 'a')
async def save_photo(msg: types.Message, bot: Bot, state: FSMContext):
    worker = msg.from_user

    # сохранить 2й файл
    user_files[worker.id].append(msg.message_id)
    # print(await dwnld_photo_or_doc(msg, bot, worker, TKN))

    await msg.reply(f"Thanks! Please wait for us to check your work.")
    # логи
    # if str(worker.id) not in admins:
    log('logs.json', worker.id, 'SENT_FILE_2')
    log('user_baza.json', EN[project]['log'], str(worker.id))
    book.setdefault(EN[project]['log'], []).append(str(worker.id))

    # Отправить файлЫ админу и ожидать приемки
    print(user_files[worker.id])
    for i in admins:
        for x in user_files[worker.id]:
            await bot.forward_message(chat_id=i, from_chat_id=worker.id, message_id=x)
        await bot.send_message(chat_id=i, text=f'Принять файлы от {worker.full_name} @{worker.username} id{worker.id}?',
                               reply_markup=keyboard_admin)

    # # запросить id исполнителя на платформе, если еще не отправлял
    # if 1:
    #     time.sleep(1)
    #     await msg.reply(f"While we are checking, please send your Prolific ID, which consists of 24 symbols.")
    #     await state.set_state(FSM.platform_user_id)

    print(worker.full_name, 'sent all files')
    print()


# # юзер отправил свой id площадки. на prolific выглядит так 5a9d64f5f6dfdd0001eaa73d
# @router.message(F.content_type.in_({'text'}), StateFilter(FSM.platform_user_id))
# async def platform_user_id(msg: types.Message, bot: Bot, state: FSMContext):
#     txt = str(msg.text)
#     worker = msg.from_user
#
#     if len(txt) == 24:
#         await msg.reply("Good! ID saved, please wait.")
#         await state.set_state(FSM.waiting_verif)
#
#         # логи
#         log('logs.json', worker.id, f'platform id {txt}')
#         book.setdefault(EN[project]['log'], []).append(str(worker.id))
#
#     else:
#         await msg.reply('It does not look like an id, try again.')
#         log('logs.json', worker.id, 'failed id')


