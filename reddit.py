from twilio.rest import Client
import os

def Message():
    client = Client()
    from_whatsapp_number = os.environ['BOTNUMBER']
    to_whatsapp_number = os.environ['ADMINNUMBER']
    client.messages.create(from = from_whatsapp_number, to = to_whatsapp_number, body = 'Hello from reddit')
