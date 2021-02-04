

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from database import initial_db_setup
from scheduler import begin_scheduler
import logging

logging.basicConfig(level=logging.WARNING)

logging.info('Starting app...')

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:database.db'
# db = SQLAlchemy(app)

initial_db_setup()
begin_scheduler()

import views

logging.info('Running app...')




