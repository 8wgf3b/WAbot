from twilio.rest import Client
import praw
import os

def topretriever(Sub= 'all', time= 'day', limit= 5, Clockcheck = False):
    try:
        reddit = praw.Reddit(client_id= os.environ['CLIENT_ID'],
                         client_secret= os.environ['CLIENT_SECRET'],
                         username= os.environ['USERNAME'],
                         password= os.environ['PASSWORD'],
                         user_agent= os.environ['USER_AGENT'])
        subreddit = reddit.subreddit(Sub)
        message = Sub + '\n\n'
        for submission in subreddit.top(time, limit= limit):
            message += submission.title + '\n' + submission.shortlink + '\n\n'
        if Clockcheck == True:
            account_sid = os.environ['ACC_SID']
            auth_token = os.environ['AUTH_TOKEN']
            client = Client(account_sid, auth_token)
            from_whatsapp_number = 'whatsapp:' + os.environ['BOTNUMBER']
            to_whatsapp_number = 'whatsapp:' + os.environ['ADMINNUMBER']
            client.messages.create(from_ = from_whatsapp_number, to = to_whatsapp_number, body = message)
            return
        return message
    except:
        pass


def randomimageretriever(Sub='all'):
    try:
        reddit = praw.Reddit(client_id= os.environ['CLIENT_ID'],
                         client_secret= os.environ['CLIENT_SECRET'],
                         username= os.environ['USERNAME'],
                         password= os.environ['PASSWORD'],
                         user_agent= os.environ['USER_AGENT'])
        subreddit = reddit.subreddit(Sub)
        submission = subreddit.random()
        return submission.title, submission.url
    except:
            pass
