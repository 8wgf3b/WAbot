from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)



@app.route('/inb', methods=['GET', 'POST'])
def reply():
    number = request.form['From']
    message_body = request.form['Body']
#    response = message_body
    message_body = message_body.split()
    if message_body[0].lower() == '!echo':
        response = ' '.join(message_body[1:])
    else:
        response = '**Bruh Moment**'
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
#    startscheduling()
    app.run()
