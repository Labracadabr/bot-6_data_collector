from aiogram import Router
from bot_logic import Access, log
from aiogram.types import Message
import json


# Инициализация
router: Router = Router()
admins: list[str] = ['992863889']
global bans

with open('user_baza.json', encoding='utf-8') as f:
    bans = json.load(f)['ban']
print(bans)

# забанить юзера по id. пример сообщения: ban 123456789
@router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
async def banner(msg: Message):
    ban_id = str(msg.text).split()[-1]
    log('user_baza.json', 'ban', ban_id)
    with open('user_baza.json', encoding='utf-8') as f:
        bans_ = json.load(f)['ban']
    bans = bans_

    await msg.answer(text=f'id {ban_id} banned')

