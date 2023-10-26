from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import get_token
import handlers


def main():
    # get bot token
    BOT_TOKEN = get_token()

    # create updater obj
    updater = Updater(BOT_TOKEN)

    # create dispatcher obj
    dp = updater.dispatcher

    # command handlers
    dp.add_handler(CommandHandler('start', handlers.start))

    # message handlers
    # dp.add_handler(MessageHandler(Filters.text, handlers.register))


    # start polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
