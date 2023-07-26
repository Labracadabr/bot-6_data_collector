import json

# для какого проекта настройки. от этого зависит, по какому сценарию бот будет отвечать
# project = 'med'
project = 'selfie'
# project = ''

# тип приемки ответов на платформе.
# если False, то verification_code выдается сразу, как юзер всё отправил, и в results сохраняется platform_id
auto_approve: bool = False

# если ручная пост-приемка, указать пример platform_id
platform_id_example: str = '5a9d64f5f6dfdd0001eaa73d'

# Кому юзер напишет в случае проблем. Встречается только в команде /help
mngr: str = '@its_dmitrii'

# список id админов
admins: list[str] = ["992863889"]

# проверочный код для опроса на платформе
verification_code: str = 'C18SJ60B'

# Куда сохранятся файлы из ответов. Заранее создать папку
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\OUTPUT\MED"
# SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\OUTPUT\SELFIE"

# Куда сохранятся id принятых ответов в случае ручной приемки:
results: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\OUTPUT\results\doc.txt"

# баны и доступы юзеров. тк я не умею в sql, то это просто json
with open('user_baza.json', encoding='utf-8') as f:
    book: dict[str, list[str]] = json.load(f)

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False
