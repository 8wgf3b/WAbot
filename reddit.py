from twilio.rest import Client
import os

def Message():
    account_sid = os.environ['ACC_SID']
    auth_token = os.environ['AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    from_whatsapp_number = 'whatsapp:' + os.environ['BOTNUMBER']
    to_whatsapp_number = 'whatsapp:' + os.environ['ADMINNUMBER']
    client.messages.create(from_ = from_whatsapp_number, to = to_whatsapp_number, body = 'Hello from reddit')
