import time
import json
import requests
import os
from aiogram import Router, Bot, F, types, Dispatcher
from aiogram.filters import Command, Text, StateFilter, or_f
# from aiogram.types import Message, CallbackQuery
from bot_logic import log, Access, FSM, dwnld_photo_or_doc
from config_data.config import Config, load_config
from keyboards import keyboard_admin, keyboard_ok, keyboard_privacy
from settings import admins, book, project, auto_approve, verification_code, platform_id_example
from lexic.lexic import EN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message


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
    # if str(worker.id) not in admins:
    log('logs.json', worker.id, 'privacy_ok')

    # выдать инструкцию и примеры
    await bot.send_message(text=EN[project]['instruct1'], chat_id=worker.id)
    # await bot.send_photo(photo=EN[project]['example_link'], caption='Examples', chat_id=worker.id)
    await bot.send_media_group(media=json.loads(EN[project]['example_json']), chat_id=worker.id)
    await bot.send_message(text=EN[project]['instruct2'], chat_id=worker.id, parse_mode='HTML')
    time.sleep(1)

    if auto_approve:
        await bot.send_message(text=EN[project]['instruct3'], chat_id=worker.id, parse_mode='HTML')
        # бот переходит в состояние ожидания первой фотки
        await state.set_state(FSM.upload_photo)

    if not auto_approve:
        # бот переходит в состояние ожидания platform_id
        await bot.send_message(text=f'First, please now send your platform ID.\nExample: {platform_id_example}',
                               chat_id=worker.id, parse_mode='HTML')
        await state.set_state(FSM.platform_user_id)


# если юзер пишет что-то не нажав ✅
@router.message(StateFilter(FSM.policy))
async def privacy_missing(msg: Message):
    log('logs.json', msg.from_user.id, 'privacy_missing')
    await msg.answer("Please accept the policy first.")


# если юзер кидает фото не отправив platform ID
@router.message(F.content_type.in_({'photo', 'document'}), StateFilter(FSM.platform_user_id))
async def platform_id_missing(msg: Message):
    log('logs.json', msg.from_user.id, 'platform_id_missing')
    await msg.answer("I am now expecting your platform ID.")


# юзер отправил свой id площадки
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.platform_user_id))
async def platform_user_id(msg: types.Message, bot: Bot, state: FSMContext):
    platform_id = str(msg.text)
    worker = msg.from_user

    if len(platform_id) == len(platform_id_example):
        # бот переходит в состояние ожидания первой фотки
        await bot.send_message(text=f"Ok! {EN[project]['instruct3']}\n\n{EN[project]['full_hd']}",
                               chat_id=worker.id, parse_mode='HTML')
        await state.set_state(FSM.upload_photo)

        # логи
        log('logs.json', worker.id, f'platform_id {platform_id}')
        book.setdefault(EN[project]['log'], []).append(str(worker.id))
        # log('user_baza.json', 'platform_ids'[worker.id], platform_id)

        # сохранить platform_id
        with open('user_baza.json', encoding='utf-8') as f:
            data = json.load(f)
        data['platform_ids'][str(worker.id)] = platform_id
        with open('user_baza.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    else:
        await msg.reply('It does not look like a correct id, try again.')
        log('logs.json', worker.id, 'failed id')


# юзер отправил альбом: не принимается
@router.message(lambda msg: msg.media_group_id)
async def alb(msg: Message):
    worker = msg.from_user
    log('logs.json', worker.id, 'album')
    await msg.reply("Please send each file in two separate messages, not as one album.")


# юзер отправил сжатые фото
@router.message(F.content_type.in_({'photo'}))
async def compressed_pic(msg: Message, bot: Bot, state: FSMContext):
    log('logs.json', msg.from_user.id, '/file')
    await msg.reply(EN[project]['full_hd'], parse_mode='HTML')


# юзер отправил 1ое фото
@router.message(F.content_type.in_({'document'}), StateFilter(FSM.upload_photo))
async def photo1(msg: Message, bot: Bot, state: FSMContext):
    worker = msg.from_user

    # сохранить первый файл
    await dwnld_photo_or_doc(msg, bot, worker, TKN)
    user_files[worker.id] = []
    user_files[worker.id].append(msg.message_id)
    log('logs.json', worker.id, 'SENT_FILE_1')

    # бот переходит в состояние ожидания 2го фото
    await state.set_state(FSM.upload_2_photo)
    await msg.reply("Good, now send the second part.")


# юзер отправил 2ое фото
@router.message(F.content_type.in_({'photo', 'document'}), StateFilter(FSM.upload_2_photo))
# @router.message(lambda msg: msg.text == 'a')
async def photo2(msg: types.Message, bot: Bot, state: FSMContext):
    worker = msg.from_user

    # сохранить 2й файл
    user_files[worker.id].append(msg.message_id)
    await dwnld_photo_or_doc(msg, bot, worker, TKN)

    if auto_approve:    # юзер ожидает проверку
        await msg.reply(f"Thanks! Please wait for us to check your work.")
        await state.set_state(FSM.waiting_verif)
        # Отправить файлЫ админу на проверку
        for i in admins:
            for pic in user_files[worker.id]:
                await bot.forward_message(chat_id=i, from_chat_id=worker.id, message_id=pic)
            await bot.send_message(chat_id=i,
                                   text=f'Принять файлы от {worker.full_name} @{worker.username} id{worker.id}?',
                                   reply_markup=keyboard_admin)

    if not auto_approve:    # Дать юзеру код
        await bot.send_message(chat_id=worker.id, text=f"Done! Here is your verification code, just click it to copy:")
        await bot.send_message(chat_id=worker.id, text=f'<code>{verification_code}</code>', parse_mode='HTML')

        # Отправить файлЫ админу на проверку
        with open('user_baza.json', 'r') as f:
            data = json.load(f)
            platform_id = data['platform_ids'][str(worker.id)]

        for i in admins:
            for pic in user_files[worker.id]:
                await bot.forward_message(chat_id=i, from_chat_id=worker.id, message_id=pic)
            await bot.send_message(chat_id=i,
                                   text=f'Принять файлы от {worker.full_name} @{worker.username} id{worker.id}?\n'
                                        f'platform_id{platform_id}',
                                   reply_markup=keyboard_admin)

    # логи
    # if str(worker.id) not in admins:
    log('logs.json', worker.id, 'SENT_FILE_2')
    log('user_baza.json', EN[project]['log'], str(worker.id))
    book.setdefault(EN[project]['log'], []).append(str(worker.id))

    print(worker.full_name, 'sent all files')
    print()


# # если юзер что-то пишет, когда бот ожидает фото
# @router.message(~Access(admins), F.content_type.in_({'text'}), or_f(StateFilter(FSM.upload_photo), StateFilter(FSM.upload_2_photo)))
# async def pics_id_missing(msg: Message):
#     log('logs.json', msg.from_user.id, 'pics_id_missing')
#     await msg.answer("I am now expecting pictures.")
