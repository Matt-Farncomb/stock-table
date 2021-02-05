

from flask import Flask
from database import create_status_table, update_databse
from scheduler import begin_scheduler, initial_db_update
import logging

logging.basicConfig(level=logging.DEBUG)

logging.info('Starting app...')

app = Flask(__name__)

create_status_table()
initial_db_update()
begin_scheduler()

import views

logging.info('Running app...')




