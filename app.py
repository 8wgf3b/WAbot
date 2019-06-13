from flask import Flask, request
import flask

from twilio.twiml.messaging_response import MessagingResponse
from reddit import topretriever, randomimageretriever
from media import echoimage, clean, sudoku
from twilio.rest import Client
from random import random
from sports import getmatches, rawreturn
import os
import telebot

app = Flask(__name__)
website = os.environ['WEBSITE']
token = os.environ['TEL_ACC_TOK']

bot = telebot.TeleBot(token)

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=website+token)
    return '!', 200

@app.route('/'+token, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '!', 200
    else:
        flask.abort(403)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@app.route('/inb', methods=['GET', 'POST'])
def reply():
    number = request.form['From']
    num_media = int(request.values.get("NumMedia"))
    message_body = request.form['Body']
    message_body = message_body.split()

    if message_body[0].lower() == '!echo':
        response = ' '.join(message_body[1:])

    elif message_body[0].lower() == '!rtop':
        response = topretriever(message_body[1], message_body[2], int(message_body[3]), False)

    elif message_body[0].lower() == '!ecim' and num_media > 0:
        media_url = request.values.get(f'MediaUrl{0}')
        resp = MessagingResponse()
        resp.message(body = 'Echoed image').media(echoimage(media_url))
        clean()
        return str(resp)

    elif message_body[0].lower() == '!sdku' and num_media > 0:
        media_url = request.values.get(f'MediaUrl{0}')
        resp = MessagingResponse()
        resp.message(body = 'sudoku').media(sudoku(media_url))
        clean()
        return str(resp)

    elif message_body[0].lower() == '!mtch':
        response = rawreturn()[:100]

    elif message_body[0].lower() == '!clen':
        response = clean(path = 'temp/', log = True)

    elif message_body[0].lower() == '!dank':
        resp = MessagingResponse()
        mess, media_url, _ = randomimageretriever(Sub='dankmemes')
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '!cohv':
        resp = MessagingResponse()
        mess, media_url, _ = randomimageretriever(Sub='comedyheaven')
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '!cpst':
        resp = MessagingResponse()
        _, media_url, mess = randomimageretriever(Sub='copypasta')
        mess = mess.encode('ascii', 'ignore').decode('ascii')
        resp.message(body = mess)
        return str(resp)

    elif message_body[0].lower() == '!joke':
        resp = MessagingResponse()
        title, _, mess = randomimageretriever(Sub='jokes')
        mess = title + '\n\n\n' + mess
        resp.message(body = mess)
        return str(resp)

    else:
        mess = ''
        lst = [str.upper, str.lower]
        for x in message_body:
            mess += ''.join(c.upper() if random() > 0.5 else c for c in x) + ' '
        media_url = 'http://i.imgur.com/nOVxxwU.jpg'
        response = '*' + mess[:-1] + '*'
        resp = MessagingResponse()
        resp.message(body = response).media(echoimage(media_url))

    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
