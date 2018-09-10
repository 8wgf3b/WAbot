from flask import Flask, request
from twilio import twiml

app = Flask(__name__)

@app.route('/inb', methods=['POST'])
def reply():
    number = request.form['From']
    message_body = request.form['Body']

    resp = twiml.Response()
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run()
