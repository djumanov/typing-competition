from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CallbackContext
from db import DB

db = DB('database.json')


def start(update: Update, conext: CallbackContext):
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz\'!')
        return
    else:
        update.message.reply_html('Assalomu alaykum ismingizni kiriting:')
    text = update.message.text
    db.add_or_update_temp_user(chat_id=user.id,)
def register(update: Update, context: CallbackContext):
    bot=context.bot
    user = update.effective_user
    text = update.message.text
    # print(text)
    temp_user=db.get_temp_user(user.id)
    step=db.get_temp_user(user.id)['step']
    if step=='first_name':
        update.message.reply_html('Familiyangizni kiriting:')
        db.add_or_update_temp_user(chat_id=user.id,first_name=text)
    if step=='last_name':
        update.message.reply_html('guruxni  kiriting:')
        db.add_or_update_temp_user(chat_id=user.id,last_name=text)
    if step=='group':
        db.add_or_update_temp_user(chat_id=user.id,group=text)
    if step=="finnal":
        ism=temp_user["first_name"]
        familiya=temp_user["last_name"]
        group=text
        button1 = InlineKeyboardButton(text = "to'gri", callback_data="done")
        button2 = InlineKeyboardButton(text = "noto'g'ri (o'zgartirish)", callback_data="edit")
        keyboard = InlineKeyboardMarkup([[button1],[button2]])
        bot.sendMessage(chat_id=user.id, text=f"Ism: {ism}\nFamiliya: {familiya}\nGurux {group}\n ", reply_markup=keyboard)
def register_save(update: Update, context: CallbackContext):
    user = update.effective_user
    step=db.get_temp_user(user.id)['step']
    if step=='finnal':
        db.add_user(chat_id=user.id)