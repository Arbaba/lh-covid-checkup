from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from datetime import datetime
from scripts import parser
import pickle
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=15)
def fetchSubmissions():
    subs = parser.allSubmissions()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("----- Fetch submissions -----")
    subsWithVideos, subsWithoutVideos  =  parser.findVideos(subs)
    data = {'time': timestamp,
            'withVideos': subsWithVideos,
            'withoutVideos': subsWithoutVideos}

    print(str(len(subs)) + " submissions fetched")
    pickle.dump(data, open("crondata.p", 'wb'))
    print("Submissions stored in crondata.p")
    
fetchSubmissions()
sched.start()