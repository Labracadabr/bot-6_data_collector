from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


privacy_en: str = "https://drive.google.com/file/d/1RddAFv77L6sL2tvPJBFxA5eI-Zb9Z1AC/view"

# кнопки как опция ответа
# button_start = KeyboardButton(text='/start')
# button_help = KeyboardButton(text='/help')

url_button = InlineKeyboardButton(text='Privacy policy', url=privacy_en)
privacy_ok = InlineKeyboardButton(text='✅', callback_data='ok_pressed')

admin_ok: InlineKeyboardButton = InlineKeyboardButton(text='✅', callback_data='admin_ok')
admin_no: InlineKeyboardButton = InlineKeyboardButton(text='❌', callback_data='admin_no')

# клавиатуры из таких кнопок
keyboard_privacy = InlineKeyboardMarkup(inline_keyboard=[[url_button]])
keyboard_ok = InlineKeyboardMarkup(inline_keyboard=[[privacy_ok]])
keyboard_admin = InlineKeyboardMarkup(inline_keyboard=[[admin_ok], [admin_no]])
