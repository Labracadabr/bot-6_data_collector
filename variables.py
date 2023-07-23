import json

# для какого проекта настройки
project = 'med'
# project = 'selfie'
# project = ''

# кому юзер напишет в случае проблем
mngr = '@its_dmitrii'

# баны и доступы юзеров. тк я не умею в sql, то это просто json
with open('user_baza.json', encoding='utf-8') as f:
    book = json.load(f)
admins: list[str] = ["992863889"]

# проверочный код для опроса на платформе
verification_code: str = 'C18SJ60B'

# куда сохранятся ответы
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\SELFIES"
