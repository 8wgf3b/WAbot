from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from reddit import topretriever
from media import echoimage, clean, sudoku
from twilio.rest import Client
import os

app = Flask(__name__)

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

    else:
        response = '*Bruh Moment*'

    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
#    startscheduling()
    app.run()
