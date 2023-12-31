
from flask import Flask
from os import path
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# db = SQLAlchemy()
# DB_NAME = "database.db"


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = secrets.token_hex(20)
  # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  # db.init_app(app)
  scheduler = BackgroundScheduler()
  from .cron import cronCall
  scheduler.add_job(cronCall, 'date', run_date=datetime.datetime.now())
  scheduler.add_job(cronCall, 'interval', hours=1, id='main')

  from .views import views
  # from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  # app.register_blueprint(auth, url_prefix='/')
  with app.app_context():
    scheduler.start()

  # from .models import User, Note

  # with app.app_context():
  #   db.create_all()

  # login_manager = LoginManager()
  # login_manager.login_view = 'auth.login'
  # login_manager.init_app(app)

  # @login_manager.user_loader
  # def load_user(id):
  #   return User.query.get(int(id))

  return app


# def create_database(app):
#   if not path.exists('website/' + DB_NAME):
#     db.create_all(app=app)
#     print('Created Database!')
