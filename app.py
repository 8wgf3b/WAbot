from flask import Flask, request, Response
import requests
import logging
from twilio.twiml.messaging_response import MessagingResponse
from reddit import topretriever, randomimageretriever
from media import echoimage, clean, sudoku
from twilio.rest import Client
from random import random
from sports import livescore
import os
#import telebot



app = Flask(__name__)
website = os.environ['WEBSITE']
token = os.environ['TEL_ACC_TOK']

@app.route('/'+token, methods=['POST'])
def telegram():
    telweb = 'https://api.telegram.org/bot'
    if request.method == 'POST':
        try:
            js = request.get_json()
            chat_id = js['message']['chat']['id']
            message_body = js['message']['text']
            message_body = message_body.split()
            if message_body[0].lower() == '/echo':
                response = ' '.join(message_body[1:])
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/rtop':
                response = topretriever(message_body[1], message_body[2], int(message_body[3]), False)
                payload = {'chat_id': chat_id, 'text': response}

            elif message_body[0].lower() == '/dank':
                mess, media_url, _ = randomimageretriever(Sub='dankmemes')
                payload = {'chat_id': chat_id, 'caption': mess, 'photo':media_url}
                r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
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

            else:
                mess = ''
                lst = [str.upper, str.lower]
                for x in message_body:
                    mess += ''.join(c.upper() if random() > 0.5 else c for c in x) + ' '
                media_url = 'http://i.imgur.com/nOVxxwU.jpg'
                response = mess[:-1]
                payload = {'chat_id': chat_id, 'caption': response, 'photo':media_url}
                r = requests.post(telweb+token+'/'+'sendPhoto', json=payload)
                return Response('ok', status=200)


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

    elif message_body[0].lower() == '/clen':
        response = clean(path = 'temp/', log = True)

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
