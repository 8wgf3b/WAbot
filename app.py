from flask import Flask, request, Response, render_template
import requests
import logging
from twilio.twiml.messaging_response import MessagingResponse
from reddit import topretriever, randomimageretriever, useranalysis, subredditanalysis
from media import echoimage, clean, sudoku
from twilio.rest import Client
from random import random, shuffle
from sports import livescore
from bigbro import relation
from db import Resub
from utils import utc
import os
import time
from db import db
from news import headlines


#import telebot



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
db.init_app(app)
website = os.environ.get('WEBSITE', '')
token = os.environ.get('TEL_ACC_TOK', '')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/')
def mainpage():
    return 'This is a personal chatbot for whatsapp and telegram'

@app.route('/termsofservice')
def tos():
    return render_template('termsfeed-terms-conditions-html-english.html')

@app.route('/ifttt', methods=['POST'])
def ifttt():
    if request.method == 'POST':
        try:
            js = request.get_json()
            telweb = 'https://api.telegram.org/bot'
            for user in Resub.getall():
                chat_id = user.chatid

                if js['action'] == 'redditroutine':
                    subs = user.subs.split()
                    shuffle(subs)
                    for sub in subs:
                        response = topretriever(sub, 'day', 10, False)
                        payload = {'chat_id': chat_id, 'text': response}
                        r = requests.post(telweb+token+'/'+'sendMessage', json=payload)

            return Response('ok', status=200)

        except Exception as e:
            print(e)
            return Response('ok', status=200)
    else:
        return Response('ok', status=200)


@app.route('/'+token, methods=['POST'])
def telegram():
    telweb = 'https://api.telegram.org/bot'
    if request.method == 'POST':
        try:
            js = request.get_json()
            chat_id = js['message']['chat']['id']
            message_body = js['message']['text']
            message_body = message_body.split()
            date = js['message']['date']
            if  time.time() - date > 60:
                return Response('ok', status=200)

            if message_body[0].endswith('@fbpa_bot'):
                message_body[0] = message_body[0][:-9]
                
            if message_body[0].lower() == '/echo':
                response = ' '.join(message_body[1:])
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/news':
                response = headlines(' '.join(message_body[1:]))
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/redreg':
                s = list(set(map(lambda x: x.lower(), message_body[1:])))
                user = Resub(str(chat_id), ' '.join(s))
                user.upsert()
                response = 'Subslist\n* ' + '\n* '.join(Resub.sublist(str(chat_id)).split())
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/redapp':
                s = list(set(map(lambda x: x.lower(), message_body[1:])))
                Resub.redappend(str(chat_id), s)
                response = 'Subslist\n* ' + '\n* '.join(Resub.sublist(str(chat_id)).split())
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/reddel':
                s = list(set(map(lambda x: x.lower(), message_body[1:])))
                Resub.redremove(str(chat_id), s)
                response = 'Subslist\n* ' + '\n* '.join(Resub.sublist(str(chat_id)).split())
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/redlist':
                response = 'Subslist\n* ' + '\n* '.join(Resub.sublist(str(chat_id)).split())
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/redtest':
                subs = Resub.sublist(str(chat_id)).split()
                shuffle(subs)
                for sub in subs:
                    response = topretriever(sub, 'day', 10, False)
                    payload = {'chat_id': chat_id, 'text': response}
                    r = requests.post(telweb+token+'/'+'sendMessage', json=payload)
                return Response('ok', status=200)

            elif message_body[0].lower() == '/rtop':
                if len(message_body) == 1:
                    response = 'example: /rtop <subreddit name> <day/week/hour/..> <number of posts>'
                else:
                    response = topretriever(*message_body[1:])
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/utc':
                response = utc(format='HOUR')
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/dank':
                mess, media_url, _ = randomimageretriever(Sub='dankmemes')
                payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                return Response('ok', status=200)

            elif message_body[0].lower() == '/curse':
                mess, media_url, _ = randomimageretriever(Sub='cursedimages')
                payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                return Response('ok', status=200)

            elif message_body[0].lower() == '/ruseran':
                if len(message_body) == 1:
                    response = 'example: /ruseran <redittor url or username>'
                    payload = {'chat_id': chat_id, 'text': response}

                else:
                    user = message_body[1].split('/')[-1]
                    media_url, m1, m2 = useranalysis(*message_body[1:])
                    mess = user + '\npost karma: '.ljust(20) + m1 + '\ncomment karma: '.ljust(20) + m2 + '\n'
                    payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                    r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                #    clean()
                    return Response('ok', status=200)

            elif message_body[0].lower() == '/rsuban':
                if len(message_body) == 1:
                    response = 'example: /rsuban <subredditname>'
                    payload = {'chat_id': chat_id, 'text': response}
                else:
                    media_url, rank = subredditanalysis(*message_body[1:])
                    mess = message_body[1] + '\n\n' + 'trending rank: ' + rank
                    payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                    r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                #    clean()
                    return Response('ok', status=200)

            elif message_body[0].lower() == '/cohv':
                mess, media_url, _ = randomimageretriever(Sub='comedyheaven')
                payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                return Response('ok', status=200)

            elif message_body[0].lower() == '/cpst':
                title, media_url, mess = randomimageretriever(Sub='copypasta')
                payload = {'chat_id': chat_id, 'text': mess}

            elif message_body[0].lower() == '/joke':
                title, media_url, mess = randomimageretriever(Sub='jokes')
                mess = title + '\n\n' + mess
                payload = {'chat_id': chat_id, 'text': mess}

            elif message_body[0].lower() == '/livc':
                mess = livescore()
                payload = {'chat_id': chat_id, 'text': mess}

            elif message_body[0].lower() == '/clam':
                mess = relation('/clam', None)['result']
                payload = {'chat_id': chat_id, 'text': mess}

        #    elif message_body[0].lower() == '/rumz':
        #        mess = relation('/rumz', message_body[1])['result']
        #        payload = {'chat_id': chat_id, 'text': mess}

            r = requests.post(telweb+token+'/'+'sendMessage', json=payload)
            return Response('ok', status=200)

        except Exception as e:
            print(e)
            return Response('ok', status=200)
    else:
        return 'hmmm'


@app.route('/inb', methods=['GET', 'POST'])
def whatsapp():
    number = request.form['From']
    num_media = int(request.values.get("NumMedia"))
    message_body = request.form['Body']
    message_body = message_body.split()

    if message_body[0].lower() == '/echo':
        response = ' '.join(message_body[1:])

    elif message_body[0].lower() == '/rtop':
        response = topretriever(message_body[1], message_body[2], int(message_body[3]), False)

    elif message_body[0].lower() == '/ecim' and num_media > 0:
        media_url = request.values.get(f'MediaUrl{0}')
        resp = MessagingResponse()
        resp.message(body = 'Echoed image').media(echoimage(media_url))
        clean()
        return str(resp)

    elif message_body[0].lower() == '/sdku' and num_media > 0:
        media_url = request.values.get(f'MediaUrl{0}')
        resp = MessagingResponse()
        resp.message(body = 'sudoku').media(sudoku(media_url))
        clean()
        return str(resp)

    elif message_body[0].lower() == '/livc':
        response = livescore()

    elif message_body[0].lower() == '/utc':
        response = utc(format = 'HOUR')

    elif message_body[0].lower() == '/clen':
        response = clean(path = 'temp/', log = True)

    elif message_body[0].lower() == '/ruseran':
        resp = MessagingResponse()
        media_url, m1, m2 = useranalysis(*message_body[1:])
        mess = 'post karma: '.ljust(20) + m1 + '\ncomment karma: '.ljust(20) + m2 + '\n'
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '/rsuban':
        resp = MessagingResponse()
        media_url, rank = subredditanalysis(*message_body[1:])
        mess = message_body[1] + '\n\n' + 'trending rank: ' + rank
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '/dank':
        resp = MessagingResponse()
        mess, media_url, _ = randomimageretriever(Sub='dankmemes')
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '/cohv':
        resp = MessagingResponse()
        mess, media_url, _ = randomimageretriever(Sub='comedyheaven')
        resp.message(body = mess).media(media_url)
        clean()
        return str(resp)

    elif message_body[0].lower() == '/cpst':
        resp = MessagingResponse()
        _, media_url, mess = randomimageretriever(Sub='copypasta')
        mess = mess.encode('ascii', 'ignore').decode('ascii')
        resp.message(body = mess)
        return str(resp)

    elif message_body[0].lower() == '/joke':
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
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
