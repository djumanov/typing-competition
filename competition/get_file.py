from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = '6504375110:AAGJ21B8tkjG6FPdPrXcWtvhQl2T6QD9Gf8'

def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    with open("custom/file.csv", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)


updater = Updater(BOT_TOKEN)

updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader))

updater.start_polling()
updater.idle()