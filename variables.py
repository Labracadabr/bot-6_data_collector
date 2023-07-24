import json

# для какого проекта настройки
project = 'med'
# project = 'selfie'
# project = ''


# Кому юзер напишет в случае проблем. Встречается только в команде /help
mngr: str = '@its_dmitrii'

# список id админов
admins: list[str] = ["992863889"]

# проверочный код для опроса на платформе
verification_code: str = 'C18SJ60B'

# куда сохранятся ответы
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\SELFIES"

# баны и доступы юзеров. тк я не умею в sql, то это просто json
with open('user_baza.json', encoding='utf-8') as f:
    book: dict[str, list[str]] = json.load(f)
