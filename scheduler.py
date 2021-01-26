from apscheduler.schedulers.background import BackgroundScheduler
from database import update_databse
import config


def background_db_updater():
    print("Scheduler is alive!")
    update_databse()
    print("database updated")


def begin_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(background_db_updater,'interval',minutes=config.refresh_interval_minutes)
    sched.start()
    print("Schedule initiated")
 
