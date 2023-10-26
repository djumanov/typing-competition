from telegram.ext import Updater, CommandHandler
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

    # start polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
