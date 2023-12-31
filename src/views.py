from .controllers import getAllServices, getService
from flask import Blueprint, render_template, request, flash, jsonify
import json
import os
from .cron import cronCall
from dotenv import load_dotenv
load_dotenv()

# from . import db
# from flask_login import login_required, current_user
# from .models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
  return render_template("index.html")


@views.route('/services', methods=['GET'])
def servicesRoute():
  ans = getAllServices()
  if ans == None:
    return "processing, please revisit after some time"
  return render_template("services.html", services=ans)


@views.route('/service/<name>', methods=['GET'])
def serviceRoute(name):
  # work on sanitization
  if not name.isalpha():
    return "err! wrong input"
  sanitizedName = name.replace("{", "").replace("}", "")
  ans = getService(sanitizedName)
  if ans == None:
    return "processing..."
  return render_template("service.html", service=ans)


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
