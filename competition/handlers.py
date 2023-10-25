from telegram.ext import Updater, MessageHandler, Filters



def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    with open("custom/file.csv", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)

