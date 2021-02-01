

from flask import Flask
from database import initial_db_setup
from scheduler import begin_scheduler
import logging

logging.basicConfig(level=logging.DEBUG)

logging.info('Starting app...')
app = Flask(__name__)
initial_db_setup()
begin_scheduler()

import views

logging.info('Running app...')




