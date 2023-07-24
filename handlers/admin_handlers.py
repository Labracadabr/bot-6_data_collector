from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from variables import verification_code, admins, book
from bot_logic import Access, log

# Инициализация
router: Router = Router()


# Забанить юзера по id. Пример сообщения: ban id123456789
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

    # убрать кнопки админа
    await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)

    # Дать юзеру код
    await bot.send_message(chat_id=worker, text=f"Success! Here is your verification code, just click it to copy:")
    await bot.send_message(chat_id=worker, text=f'<code>{verification_code}</code>', parse_mode='HTML')


# admin нажал ❌
@router.callback_query(Text(text=['admin_no']))
async def admin_no(callback: CallbackQuery, bot: Bot):
    msg = callback.message

    # обновить сообщение у админа и убрать кнопки
    await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Напиши причину отказа ответом на это сообщение!',
                                msg.chat.id, msg.message_id, reply_markup=None)


# Причина отказа
@router.message(Access(admins), lambda msg: msg.reply_to_message)
async def reply_decline_reason(m: Message, bot: Bot):
    # worker = вытащить id из текста сообщения
    txt = str(m.reply_to_message.text).split()
    for i in txt:
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    # сообщение, на которое отвечаем
    orig = m.reply_to_message

    # обновить сообщение у админа и дописать причину отказа
    await bot.edit_message_text(f'❌ Отклонено. Причина:\n{m.text}', orig.chat.id, orig.message_id, reply_markup=None)

    # сообщить юзеру об отказе
    await bot.send_message(chat_id=worker, text=f'Your file has been rejected. Reason:\n\n<i>{m.text}</i>', parse_mode='HTML')

