from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from variables import verification_code, admins, book, auto_approve, results
from bot_logic import Access, log
import json

# Инициализация
router: Router = Router()


# Забанить юзера по telegram id. Пример сообщения: ban id123456789
@router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
async def banner(msg: Message):
    # вытащить id из текста сообщения
    ban_id = str(msg.text).split()[-1]
    if ban_id.lower().startswith('id'):
        ban_id = ban_id[2:]

    # ведение учета
    log('user_baza.json', 'ban', ban_id)
    book.setdefault('ban', []).append(ban_id)

    await msg.answer(text=f'id {ban_id} banned')


# admin нажал ✅
@router.callback_query(Text(text=['admin_ok']))
async def admin_ok(callback: CallbackQuery, bot:Bot):
    msg = callback.message

    # вытащить id из текста сообщения
    for i in str(msg.text).split():
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    if auto_approve:
        # убрать кнопки админа
        await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)
        # Дать юзеру код
        await bot.send_message(chat_id=worker, text=f"Success! Here is your verification code, just click it to copy:")
        await bot.send_message(chat_id=worker, text=f'<code>{verification_code}</code>', parse_mode='HTML')

    if not auto_approve:
        # вытащить platform_id из текста сообщения
        for i in str(msg.text).split():
            if i.lower().startswith('platform_id'):
                platform_id = i[11:]
                break

        with open(results, 'w', encoding='utf-8') as f:
            f.writelines(f'{platform_id}, +\n')
        # убрать кнопки админа
        await bot.edit_message_text(f'{msg.text}\n✅ Принято. Platform_id сохранен.',
                                    msg.chat.id, msg.message_id, reply_markup=None)


# admin нажал ❌
@router.callback_query(Text(text=['admin_no']))
async def admin_no(callback: CallbackQuery, bot: Bot):
    msg = callback.message

    if auto_approve:
        # обновить сообщение у админа и убрать кнопки
        await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Напиши причину отказа ответом на это сообщение!',
                                    msg.chat.id, msg.message_id, reply_markup=None)

    if not auto_approve:
        # вытащить platform_id из текста сообщения
        for i in str(msg.text).split():
            if i.lower().startswith('platform_id'):
                platform_id = i[11:]
                break

        with open(results, 'a') as f:
            f.writelines(f'{platform_id}, -\n')
        # обновить сообщение у админа и убрать кнопки
        await bot.edit_message_text(f'{msg.text}\n❌ Отклонено. Platform_id сохранен.\n\n'
                                    f'Напиши причину отказа ответом на это сообщение!',
                                    msg.chat.id, msg.message_id, reply_markup=None)


# Причина отказа
@router.message(Access(admins), lambda msg: msg.reply_to_message)
async def reply_decline_reason(msg: Message, bot: Bot):
    # причина отказа
    reason = str(msg.text)

    # worker = вытащить id из текста сообщения
    txt = str(msg.reply_to_message.text).split()
    for i in txt:
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    # сообщение, на которое отвечаем
    orig = msg.reply_to_message

    # обновить сообщение у админа и дописать причину отказа
    await bot.edit_message_text(f'❌ Отклонено. Причина:\n{reason}', orig.chat.id, orig.message_id,
                                reply_markup=None)

    if auto_approve:
        # обновить сообщение у админа и дописать причину отказа
        await bot.edit_message_text(f'❌ Отклонено. Причина:\n{reason}', orig.chat.id, orig.message_id,
                                    reply_markup=None)
        # сообщить юзеру об отказе
        await bot.send_message(chat_id=worker, text=f'Your file has been rejected. Reason:\n\n<i>{reason}</i>',
                               parse_mode='HTML')

    if not auto_approve:
        # вытащить platform_id из текста сообщения
        with open('user_baza.json') as f:
            platform_id = json.load(f)['platform_ids'][worker]

        with open(results, 'w') as f:
            f.writelines(f'{platform_id}, -, {reason}\n')
        # обновить сообщение у админа и убрать кнопки
        await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Platform_id сохранен. Причина:\n{reason}\n.',
                                    orig.chat.id, orig.message_id, reply_markup=None)


