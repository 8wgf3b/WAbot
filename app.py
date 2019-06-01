from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from reddit import topretriever
from media import echoimage
from twilio.rest import Client
import os

app = Flask(__name__)

@app.route('/inb', methods=['GET', 'POST'])
def reply():
    number = request.form['From']
    num_media = int(request.values.get("NumMedia"))
    message_body = request.form['Body']
#    response = message_body
    message_body = message_body.split()
    if message_body[0].lower() == '!echo':
        response = ' '.join(message_body[1:])
    elif message_body[0].lower() == '!rtop':
        response = topretriever(message_body[1], message_body[2], int(message_body[3]), False)
    elif message_body[0].lower() == '!ecim' and num_media > 0:
        output_urls = []
        for idx in range(num_media):
            media_url = request.values.get(f'MediaUrl{idx}')
            output_urls.append(echoimage(media_url))
        account_sid = os.environ['ACC_SID']
        auth_token = os.environ['AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        from_whatsapp_number = 'whatsapp:' + os.environ['BOTNUMBER']
        to_whatsapp_number = 'whatsapp:' + number
        return client.messages.create(media_url= output_urls, from_ = from_whatsapp_number, to = to_whatsapp_number, body = 'ECHOED IMG')

    else:
        response = '*Bruh Moment*'
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
#    startscheduling()
    app.run()
