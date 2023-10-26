from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, conext: CallbackContext):
    update.message.reply_html(f'Assalomu alaylum <b>{update.effective_user.full_name}</b>!')
    update.message.reply_html('Ismingizni kiriting?')
