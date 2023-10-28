from flask import Flask, jsonify, request
from handlers import db
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from settings import get_token
import handlers
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

bot = Bot(get_token())
dp = Dispatcher(bot, None, workers=0)


@app.route('/results/', methods=['GET'])
def get_results():
    return jsonify(db.get_all_results())


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return '<h1>Webhook is working...!</h1>'

    if request.method == 'POST':
        body = request.get_json()
        
        update = Update.de_json(body, bot)

        # command handlers
        dp.add_handler(CommandHandler('start', handlers.start))

        # message handlers
        dp.add_handler(MessageHandler(Filters.text, handlers.register))
        dp.add_handler(MessageHandler(Filters.document, handlers.downloader))

        # callback query handlers
        dp.add_handler(CallbackQueryHandler(handlers.register_save, pattern="done"))
        dp.add_handler(CallbackQueryHandler(handlers.register_edit, pattern="edit"))

        dp.process_update(update)

        return {'message': 'ok'}


if __name__ == '__main__':
    app.run(debug=True)

