#!/usr/bin/env python

import telegram
from flask import Flask, request

app = Flask(__name__)

token = '566786956:AAEACP90bJLHhl0jrvTcuONCRWsZ_F16G2s'
bot = telegram.Bot(token=token)

WEBHOOK_HOST = 'echo-219615.appspot.com'
WEBHOOK_PORT = 8443 # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        # repeat the same message back (echo)
        bot.sendMessage(chat_id=chat_id, text=text)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'
