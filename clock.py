from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from reddit import Message as RMessage
import time
import datetime

def startscheduling():
    scheduler = BackgroundScheduler()
    scheduler.add_job(RMessage, trigger = CronTrigger(minute='*/01'))
    scheduler.start()


if __name__ == '__main__':
    startscheduling()
