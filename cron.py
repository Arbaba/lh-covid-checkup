from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import pickle
from store import storeSubmissions
from datetime import datetime
from scripts import parser
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=15)
def cronStrore():
    storeSubmissions()

storeSubmissions()
sched.start()