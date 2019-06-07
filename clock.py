from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from reddit import topretriever
import time
import datetime
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

sched = BlockingScheduler()

sched.add_job(lambda: topretriever('datascience', 'day', 10, True), 'cron', hour='5', minute='10')
sched.add_job(lambda: topretriever('cscareerquestions', 'day', 10, True), 'cron', hour='5', minute='8')
sched.add_job(lambda: topretriever('machinelearning', 'day', 10, True), 'cron', hour='5', minute='14')
sched.add_job(lambda: topretriever('statistics', 'day', 10, True), 'cron', hour='5', minute='12')
sched.add_job(lambda: topretriever('raspberry_pi', 'day', 10, True), 'cron', hour='5', minute='6')
#sched.add_job(lambda: topretriever('raspberry_pi', 'day', 10, True), 'cron', hour='5', minute='6')
sched.add_job(lambda: topretriever('python', 'day', 10, True), 'cron', hour='5', minute='20')






sched.start()
while __name__ == '__main__':
    pass
