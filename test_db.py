# from db import DB

# db = DB('database.json')

# def test_add_or_update_temp_user():
#     print(db.add_or_update_temp_user(chat_id='1234', group="Vaiyev"))

# def test_add_user():
#     db.add_user('1234')

# test_add_user()

from telegram import Bot
from settings import get_token

bot = Bot(get_token())

print(bot.set_webhook('https://djumanov.pythonanywhere.com/webhook'))
