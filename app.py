from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from reddit import Message as RMessage

app = Flask(__name__)

def startscheduling():
    scheduler = BackgroundScheduler()
    scheduler.add_job(RMessage, 'interval', minutes = 3)
    scheduler.start()

@app.route('/inb', methods=['GET', 'POST'])
def reply():
    number = request.form['From']
    message_body = request.form['Body']
    response = message_body
    resp = MessagingResponse()
    resp.message(response)
    return str(resp)

if __name__ == '__main__':
    startscheduling()
    app.run(use_reloader=False)
