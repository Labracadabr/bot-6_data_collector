import time
import json
import os
from aiogram import Router, Bot, F, types, Dispatcher
from aiogram.filters import Command, StateFilter, or_f
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
@router.callback_query(lambda x: x.data == "ok_pressed", StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    worker = callback.from_user

    print(callback.model_dump_json(indent=4, exclude_none=True))

    # логи
    # if str(worker.id) not in admins:
    log('logs.json', worker.id, 'privacy_ok')

    # выдать инструкцию и примеры
    await bot.send_message(text=EN[project]['instruct1'], chat_id=worker.id)
    await bot.send_photo(photo=EN[project]['example_link'], caption='Examples', chat_id=worker.id)
    await bot.send_message(text=EN[project]['instruct2'], chat_id=worker.id, parse_mode='HTML')
    time.sleep(2)
    await bot.send_message(text=f"{EN[project]['instruct3']}\n\n{EN[project]['full_hd']}",
                           chat_id=worker.id, parse_mode='HTML')
    # бот переходит в состояние ожидания первой фотки
    await state.set_state(FSM.upload_photo)


# если юзер пишет что-то не нажав ✅
@router.message(StateFilter(FSM.policy))
async def privacy_missing(msg: Message):
    log('logs.json', msg.from_user.id, 'privacy_missing')
    await msg.answer("Please accept the policy first.")


# юзер отправил сжатые фото
@router.message(F.content_type.in_({'photo'}))
async def compressed_pic(msg: Message):
    log('logs.json', msg.from_user.id, '/file')
    await msg.reply(EN[project]['full_hd'], parse_mode='HTML')


# юзер отправил несжатое фото
@router.message(F.content_type.in_({'document'}), StateFilter(FSM.upload_photo))
async def photo1(msg: Message, bot: Bot, state: FSMContext):
    worker = msg.from_user
    msg_time = str(msg.date.date())+'_'+str(msg.date.time()).replace(':', '-')

    await dwnld_photo_or_doc(msg, bot, worker, TKN)

    await msg.reply(f"Thanks! Please wait for us to check your work.")

    # логи
    # if str(worker.id) not in admins:
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

