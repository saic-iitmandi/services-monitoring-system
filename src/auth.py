from flask import Blueprint, session, url_for, redirect
from .models import User
from . import db, google


auth = Blueprint('auth', __name__)


# Routes
@auth.route('/login')
def login():
  return google.authorize_redirect(url_for('auth.authorize', _external=True))


@auth.route('/authorize')
def authorize():
  token = google.authorize_access_token()
  user_info = token['userinfo']
  print(user_info['email'])
  next = session.get("next")
  session.pop('next', None)

  session['user'] = user_info
  session.permanent = True
  return redirect(next or url_for("views.servicesRoute"))


@auth.route('/logout')
def logout():
  session.pop('user', None)
  return 'Logged out successfully'
