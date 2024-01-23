from .controllers import getAllServices, getService
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import json
import os
<<<<<<< HEAD
import datetime
from .cron import cronCall

=======
from .cron import cronCall
>>>>>>> 9102e6bcf71435ee1c6924b10a503e496e3c9822
from dotenv import load_dotenv
load_dotenv()

# from . import db
# from flask_login import login_required, current_user
# from .models import Note

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
