
from flask import Flask
from os import path
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"

oauth = OAuth()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid profile email'},
)


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = secrets.token_hex(20)
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)
  oauth.init_app(app)
  scheduler = BackgroundScheduler()
  from .cron import cronCall
  scheduler.add_job(cronCall, 'date', run_date=datetime.datetime.now())
  scheduler.add_job(cronCall, 'interval', hours=1, id='main')

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  with app.app_context():
    scheduler.start()

  with app.app_context():
    db.create_all()

  return app


def create_database(app):
  if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created Database!')
