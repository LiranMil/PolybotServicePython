import flask
from flask import request
import os
from bot import QuoteBot
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
BOT_APP_URL = os.environ['BOT_APP_URL']

if not TELEGRAM_BOT_TOKEN or not BOT_APP_URL:
    raise RuntimeError("TELEGRAM_BOT_TOKEN and BOT_APP_URL must be set.")

@app.route('/', methods=['GET'])
def index():
    return 'Ok'

@app.route(f'/{TELEGRAM_BOT_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    try:
        bot.handle_message(req['message'])
    except Exception as e:
        print(f"Error handling message: {e}")
    return 'Ok'

if __name__ == "__main__":
    bot = bot(TELEGRAM_BOT_TOKEN, BOT_APP_URL)
    app.run(host='0.0.0.0', port=8443)
