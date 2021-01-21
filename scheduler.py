from apscheduler.schedulers.background import BackgroundScheduler
from database import update_databse


def background_db_updater():
    print("Scheduler is alive!")
    update_databse()
    print("database updated")


def begin_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(background_db_updater,'interval',minutes=1)
    sched.start()
    print("Schedule initiated")
 
