from telegram import Update
from telegram.ext import CallbackContext
from db import DB

db = DB('database.json')


def start(update: Update, conext: CallbackContext):
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz\'!')
        return

    db.add_or_update_temp_user(chat_id=user.id,)

