from .models import Ticket
from . import db
from .controllers import getAllServices, getService
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
import json
import os
import datetime
from .cron import cronCall

from dotenv import load_dotenv
load_dotenv()

# from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
  return redirect(url_for('views.servicesRoute'))


@views.route('/services', methods=['GET'])
def servicesRoute():
  ans = getAllServices()
  if ans == None:
    return "processing, please revisit after some time"
  return render_template("index.html", services=ans)


@views.route('/service/<name>', methods=['GET'])
def serviceRoute(name):
  # work on sanitization
  if not name.isalpha():
    return "err! wrong input"
  sanitizedName = name.replace("{", "").replace("}", "")

  ans = getService(sanitizedName)
  today = datetime.datetime.now()
  past_days = [today - datetime.timedelta(days=i) for i in range(90)]

  # Convert downtime data to graph data
  graph_data = []
  for day in past_days:
    is_down = any(
      datetime.datetime.strptime(downtime['startTime'], '%Y-%m-%d %H:%M:%S') <= day and
      datetime.datetime.strptime(
        downtime.get('endTime', today.strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S') >= day - datetime.timedelta(days=1)
        for downtime in ans['downTime']
    )
    graph_data.append({
        'color': 'red' if is_down else 'green',
        'tooltip': f'{day.strftime("%Y-%m-%d")}: {"Down" if is_down else "Up"}',
    })
  graph_data.reverse()
  if ans == None:
    return "processing..."
  return render_template("service.html", service={**ans, 'graph': graph_data})


@views.route('/api/update', methods=['GET'])
def updateStatusManually():
  # this function expects a JSON from the INDEX.js file
  password = request.args.get("pass")
  if password != os.environ.get("ADMIN_PASSWORD", ""):
    return "chle ja bhai"
  try:
    cronCall()
    return "updated"
  except:
    return "some error occured"


@views.route('/ticket', methods=['GET', 'POST'])
def newTicket():

    # user = session['user']
    # print(user)
  if session.get("user", None) != None:
    user = session['user']

    if request.method == 'POST':
      content = request.form['content']
      title = request.form['title']
      new_ticket = Ticket(content=content, title=title,
                          email=user["email"], oauth_id=user["sub"])
      try:
        db.session.add(new_ticket)
        db.session.commit()
        return redirect('/ticket')

      except:
        return 'errorrrr'

    return render_template('ticket.html')
  else:

    session["next"] = "/ticket"
    return redirect(url_for("auth.login"))
