from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/inb', methods=['GET', 'POST'])
def reply():
    number = request.form['From']
    message_body = request.form['Body']

    resp = MessagingResponse()
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run()
