import os

import requests
from flask import Flask, Response, request

app = Flask(__name__)
# Get BOT Token from telegram
token = os.environ['TELEGRAM_BOT_TOKEN']


# https://api.telegram.org/bot{token}/setWebhook?url=https://telebot-college-test.ridwaanhall.repl.co/
def generate_answer(question):
  request = question
  return request


# To Get Chat ID and message which is sent by client
def message_parser(message):
  chat_id = message['message']['chat']['id']
  if 'text' in message['message']:
    text = message['message']['text']
    print("Chat ID: ", chat_id)
    print("Message: ", text)
    return chat_id, text
  else:
    print("Chat ID: ", chat_id)
    print("Message does not contain text.")
    return chat_id, "Message does not contain text."


# To send message using "SendMessage" API
def send_message_telegram(chat_id, text):
  url = f'https://api.telegram.org/bot{token}/sendMessage'
  payload = {'chat_id': chat_id, 'text': text}
  response = requests.post(url, json=payload)
  return response


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    msg = request.get_json()
    chat_id, incoming_que = message_parser(msg)
    answer = generate_answer(incoming_que)
    send_message_telegram(chat_id, answer)
    return Response('ok', status=200)
  else:
    return "<h1>Something went wrong</h1>"
