from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from reddit import Message as RMessage
import time
import datetime

sched = BlockingScheduler()

sched.add_job(RMessage, 'interval', minutes = 5)



sched.start()
