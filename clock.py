from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from reddit import topretriever
import time
import datetime
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

sched = BlockingScheduler()

sched.add_job(lambda: topretriever('datascience', 'day', 5, True), 'cron', hour='3', minute='10')
sched.add_job(lambda: topretriever('cscareerquestions', 'day', 5, True), 'cron', hour='3', minute='8')
sched.add_job(lambda: topretriever('machinelearning', 'day', 5, True), 'cron', hour='3', minute='14')
sched.add_job(lambda: topretriever('statistics', 'day', 5, True), 'cron', hour='3', minute='12')
sched.add_job(lambda: topretriever('raspberry_pi', 'day', 5, True), 'cron', hour='3', minute='6')

sched.add_job(lambda: topretriever('datascience', 'hour', 3, True), 'cron', hour='1-19', minute='25')
sched.add_job(lambda: topretriever('cscareerquestions', 'hour', 2, True), 'cron', hour='1-19', minute='20,50')
sched.add_job(lambda: topretriever('machinelearning', 'hour', 2, True), 'cron', hour='1-19', minute='27')
sched.add_job(lambda: topretriever('statistics', 'hour', 3, True), 'cron', hour='1-19', minute='33')
sched.add_job(lambda: topretriever('raspberry_pi', 'hour', 3, True), 'cron', hour='1-19', minute='35')





sched.start()
while __name__ == '__main__':
    pass
