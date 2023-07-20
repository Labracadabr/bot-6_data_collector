import json


book: dict = {}


# Запись данных item в указанный json file по ключу key
def log(file, key, item):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    data.setdefault(key, []).append(item)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
# не рабочий варик
# def log(file, key, item):
#     with open(file, encoding='utf-8') as f1, open(file, 'w', encoding='utf-8') as f2:
#         data = json.load(f1)
#         data.setdefault(key, []).append(item)
#         json.dump(data, f2, indent=2, ensure_ascii=False)


#  Палит админу действия юзеров. Первые три аргумента вписать такими, как есть тут
async def intel(bot, message, admins, silence: bool):
    user = str(message.from_user.id)
    if user not in admins:
        for i in admins:
            await bot.send_message(text=f'{message.text} id{user} {message.from_user.full_name}'
                                        f' @{message.from_user.username}', chat_id=i, disable_notification=silence)



