import json

# баны и доступы юзеров
with open('user_baza.json', encoding='utf-8') as f:
    book = json.load(f)

admins: list[str] = ["992863889"]

# проверочный код для опроса на платформе
verification_code: str = 'C18SJ60B'

# куда сохранятся ответы
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\SELFIES"

# где хранятся примеры
SAMPLE: str = 'https://i.ibb.co/z89YvcS/collage.jpg'

