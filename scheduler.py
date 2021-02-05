from apscheduler.schedulers.background import BackgroundScheduler
from database import update_databse
import config
import logging


def background_db_updater():
    logging.info('Scheduled update running...')
    update_databse()
    logging.info('"Database updated')

def initial_db_update():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(background_db_updater)
    sched.start()

def begin_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(background_db_updater,'interval',minutes=config.refresh_interval_minutes)
    sched.start()

 
