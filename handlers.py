from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CallbackContext
from db import DB
import csv
from datetime import datetime
import requests
from io import StringIO


db = DB('database.json')


def start(update: Update, conext: CallbackContext):
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz!')
        return

    update.message.reply_text(
        text=f'Assalomu alaykum {user.full_name}! Typing bo\'yicha musoqabaqada ishtirok etish uchun ro\'yxatdan o\'ting.')
    update.message.reply_html(f'Ismingizni?')

    db.add_or_update_temp_user(chat_id=user.id)


def register(update: Update, context: CallbackContext):
    user = update.effective_user
    if db.is_user(chat_id=user.id):
        update.message.reply_html('Siz ro\'yxatdan o\'tgansiz!')
        return
    
    text = update.message.text
    temp_user=db.get_temp_user(user.id)
    step = temp_user['step']

    if step=='first_name':
        update.message.reply_html('Familiyangiz?')
        db.add_or_update_temp_user(chat_id=user.id,first_name=text)
    if step=='last_name':
        update.message.reply_html("Gruxingiz? (<i>agar yo'q bo'lsa, Yo'q deb yozing.</i>)")
        db.add_or_update_temp_user(chat_id=user.id,last_name=text)
    if step=='group':
        db.add_or_update_temp_user(chat_id=user.id,group=text)
        ism=temp_user["first_name"]
        familiya=temp_user["last_name"]
        group=text

        button1 = InlineKeyboardButton(text = "Tasdiqlash", callback_data="done")
        button2 = InlineKeyboardButton(text = "Qayta o'tish", callback_data="edit")
        keyboard = InlineKeyboardMarkup([[button1],[button2]])

        update.message.reply_html(text=f"<b>Ism:</b> {ism}\n<b>Familiya:</b> {familiya}\n<b>Gurux:</b> {group}\n\nMa'lumotlaringiz to'g'ri bo'lsa <b>Tasdiqlash</b> tugmasini bosing, ask holda <b>Qayta o'tish</b>.", reply_markup=keyboard)

    if step=="finnal":
        usr = db.get_temp_user(chat_id=user.id)

        ism=usr["first_name"]
        familiya=usr["last_name"]
        group=usr["group"]
        
        button1 = InlineKeyboardButton(text = "Tasdiqlash", callback_data="done")
        button2 = InlineKeyboardButton(text = "Qayta o'tish", callback_data="edit")
        keyboard = InlineKeyboardMarkup([[button1],[button2]])

        update.message.reply_html(text=f"<b>Ism:</b> {ism}\n<b>Familiya:</b> {familiya}\n<b>Gurux:</b> {group}\n\nMa'lumotlaringiz to'g'ri bo'lsa <b>Tasdiqlash</b> tugmasini bosing, ask holda <b>Qayta o'tish</b>.", reply_markup=keyboard)

        
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
    
    update.callback_query.message.reply_html('Ismingiz?')

    update.callback_query.delete_message()


def downloader(update: Update, context: CallbackContext):

    user = update.effective_user

    if db.is_user(chat_id=user.id):
        db_user = db.users.get(doc_id=user.id)

        response = requests.get(context.bot.get_file(update.message.document).file_path)

        csv_content = response.content.decode()

        results = list(csv.DictReader(StringIO(csv_content), delimiter='|'))

        if not results:
            update.message.reply_html(
                text=f"Siz boshqa file yubordingiz."
            )
            return 

        last_result = results[0]

        wpm = last_result['wpm']
        acc = last_result['acc']
        consistency = last_result['consistency']

        date = datetime.fromtimestamp(int(last_result['timestamp']) // 100)

        if db.add_result(
            chat_id=user.id, 
            first_name=db_user['first_name'], 
            last_name=db_user['last_name'], 
            group=db_user['group'], 
            wpm=float(wpm), 
            accuracy=float(acc), 
            consistency=float(consistency), 
            date=str(date)):

            update.message.reply_html(
                text=f"Sizning natijangiz:\n\n<b>tezlik: </b>{wpm}\n<b>xatosizlik: </b>{acc}%\n<b>doimiylik: </b>{consistency}%\n\nIshtirokingiz uchun tashakkur!"
            )
            update.message.reply_html(
                text=f"Tez orada natijalarni e'lon qilamiz."
            )
        else:
            update.message.reply_html(
                text=f"Ikkinchi urunish qabul qilinmaydi."
            )
    else:
        update.message.reply_html(
            text=f"Ro'yxatdan o'tmagansiz."
        )


def go(update: Update, context: CallbackContext):
    
    chat_ids = [user['chat_id'] for user in db.results.all()]
    users = db.users.all()

    qatnashuvchilar = ""

    for user in users:
        if user['chat_id'] not in chat_ids:
            context.bot.send_message(
                chat_id=user['chat_id'],
                text="<b>Musobaqa shartlari bilan tanishing.</b>\n\n1. monkeytype.com sayti orqali\n2. Typing davomiyligini 2 minut\n3. Bajarildan so'ng profile-dan natijalarni yublash va 2 minut ichida faylni yuborish\n\n<i>Omad!</i>",
                parse_mode='HTML'
            )
            qatnashuvchilar += user['first_name'] + " " + user['last_name'] + "\n"

    if qatnashuvchilar == "":
        update.message.reply_text("xech kim yoq")
        return

    update.message.reply_text(qatnashuvchilar)
    update.message.reply_text(
        text="<b>Musobaqa shartlari bilan tanishing.</b>\n\n1. monkeytype.com sayti orqali\n2. Typing davomiyligini 2 minut\n3. Bajarildan so'ng profile-dan natijalarni yublash va 2 minut ichida faylni yuborish\n\n<i>Omad!</i>",
    )
    update.message.reply_text("Yuborildi")
