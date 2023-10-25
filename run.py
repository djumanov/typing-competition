from telegram.ext import Updater, MessageHandler, Filters
from competition import handlers
from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

updater = Updater(BOT_TOKEN)

updater.dispatcher.add_handler(MessageHandler(Filters.document, handlers.downloader))

updater.start_polling()
updater.idle()