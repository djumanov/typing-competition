from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CallbackContext
from db import DB
import csv
from datetime import datetime
import os


db = DB('database.json')


def get_result(): 

    with open('custom/results.csv') as csvfile:
        print(csvfile.read())
        dict_reader = csv.DictReader(csvfile, delimiter='|')

        results = list(dict_reader)

        if not results:
            return False

        last_result = results[0]

        date = datetime.fromtimestamp(int(last_result['timestamp']) // 100)

        return float(last_result['wpm']), float(last_result['acc']), float(last_result['consistency']), str(date)


def start(update: Update, conext: CallbackContext):
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz\'!')
        return

    update.message.reply_html('Assalomu alaykum ismingizni kiriting:')

    db.add_or_update_temp_user(chat_id=user.id)


def register(update: Update, context: CallbackContext):
    bot=context.bot
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz\'!')
        return
    
    text = update.message.text
    temp_user=db.get_temp_user(user.id)
    step = temp_user['step']

    if step=='first_name':
        update.message.reply_html('Familiyangizni kiriting:')
        db.add_or_update_temp_user(chat_id=user.id,first_name=text)
    if step=='last_name':
        update.message.reply_html('guruxni  kiriting:')
        db.add_or_update_temp_user(chat_id=user.id,last_name=text)
    if step=='group':
        db.add_or_update_temp_user(chat_id=user.id,group=text)
        ism=temp_user["first_name"]
        familiya=temp_user["last_name"]
        group=text

        button1 = InlineKeyboardButton(text = "Tasdiqlash", callback_data="done")
        button2 = InlineKeyboardButton(text = "Inkon qilish", callback_data="edit")
        keyboard = InlineKeyboardMarkup([[button1],[button2]])

        bot.sendMessage(chat_id=user.id, text=f"Ism: {ism}\nFamiliya: {familiya}\nGurux {group}\n ", reply_markup=keyboard)

    if step=="finnal":
        usr = db.get_temp_user(chat_id=user.id)
        
        button1 = InlineKeyboardButton(text = "Tasdiqlash", callback_data="done")
        button2 = InlineKeyboardButton(text = "Inkon qilish", callback_data="edit")
        keyboard = InlineKeyboardMarkup([[button1],[button2]])

        bot.sendMessage(chat_id=user.id, text=f"Ism: {usr['first_name']}\nFamiliya: {usr['last_name']}\nGurux {usr['group']}\n ", reply_markup=keyboard)

        
def register_save(update: Update, context: CallbackContext):
    user = update.effective_user
    step=db.get_temp_user(user.id)['step']
    if step=='finnal':
        db.add_user(chat_id=user.id)
        update.callback_query.answer(text='Muvoffaqiyatli ro\'yxatdan o\'tdingiz.', show_alert=True)
        update.callback_query.delete_message()

        
def register_edit(update: Update, context: CallbackContext):
    user = update.effective_user
    
    db.clear_temp_user(chat_id=user.id)
    
    update.callback_query.message.reply_html('Ismingizni kiriting:')

    update.callback_query.delete_message()


def downloader(update: Update, context: CallbackContext):

    user = update.effective_user

    if db.is_user(chat_id=user.id):
        db_user = db.users.get(doc_id=user.id)
        with open("custom/results.csv", 'wb') as f:
            x = context.bot.get_file(update.message.document).download(out=f)

            
            c = get_result()
            if c == False:
                update.message.reply_html(
                    text=f"Boshqa fayl tashaldi."
                )
                return

            wpm, acc, consistency, date = c


            r = db.add_result(chat_id=user.id, first_name=db_user['first_name'], last_name=db_user['last_name'], group=db_user['group'], wpm=wpm, accuracy=acc, consistency=consistency, date=date)

            if r:
                update.message.reply_html(
                    text=f"Sizning natijangiz:\n\n<b>tezlik: </b>{wpm}\n<b>xatosizlik: </b>{acc}\n<b>doimiylik: </b>{consistency}\n\nIshtirokingiz uchun tashakkur!"
                )
            else:
                update.message.reply_html(
                    text=f"Ikkinchi urunish qabul qilinmaydi."
                )
    else:
        update.message.reply_html(
            text=f"Ro'yxatdan o'tmagansiz."
        )