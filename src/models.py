from . import db
# from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  oauth_id = db.Column(db.String(50), unique=True, nullable=False)
  # notes = db.relationship('Note')


class Ticket(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150))
  oauth_id = db.Column(db.String(50), nullable=False)
  content = db.Column(db.String(200), nullable=False)
  title = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
