from flask import Blueprint, session, url_for, redirect
from .models import User
from . import db, google


auth = Blueprint('auth', __name__)


# Routes
@auth.route('/login')
def login():
  return google.authorize_redirect(url_for('auth.authorize', _external=True, _scheme='https'))


@auth.route('/authorize')
def authorize():
  token = google.authorize_access_token()
  user_info = token['userinfo']
  # user = User.query.filter_by(oauth_id=user_info['sub']).first()
  print(user_info['email'])
  # if not user:
  #     user = User(google_id=user_info['sub'], name=user_info['name'], email=user_info['email'])
  #     db.session.add(user)
  #     db.session.commit()

  session['user'] = user_info
  return redirect(url_for('views.servicesRoute'))


@auth.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for("views.servicesRoute"))
