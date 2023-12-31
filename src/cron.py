# cron job to update the status of the services
import json
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import os
from dotenv import load_dotenv
load_dotenv()

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
ENDC = '\033[0m'


def coloredPrint(text, color):
  print(color + text + ENDC)


def checkStatus(inp):
  service = inp['service']
  oldDownTime = inp['downTime']
  status = {
    "name": service['dns'],
    "link": service['dns'] + '.iitmandi.co.in',
    "port": service['port'],

    "dnsStatus": 0,
    "dockerStatus": 0,
    "remark": "DOWN",
    'downTime': oldDownTime
  }
  # print("checking status of ", service['dns'])
  now = datetime.datetime.now()
  try:
    if service['dns'] == "iitmandi.co.in;":
      r = requests.get(
          "https://iitmandi.co.in", timeout=3)
      status['link'] = "iitmandi.co.in"
    else:
      r = requests.get(
          "https://" + service['dns'] + ".iitmandi.co.in", timeout=3)
    status['dnsStatus'] = r.status_code
  except requests.exceptions.ConnectionError:
    pass
  except:
    print("issue with connction via domain, status:\n", status)

  try:
    r = requests.get("http://" + os.environ.get('SITE_HOST_IP', "14.139.34.11") + ":" +
                     str(service['port']), timeout=3)
    status['dockerStatus'] = r.status_code
    # print(r.status_code)
  except requests.exceptions.ConnectionError:
    pass
  except:
    print("issue with connction via port, status:\n", status)

  if 200 <= status['dnsStatus'] < 300 and 200 <= status['dockerStatus'] < 300:
    status['remark'] = "UP"
    latestDownTime = oldDownTime.pop() if len(oldDownTime) > 0 else None
    if latestDownTime != None and latestDownTime.get('endTime', None) == None:
      newDownTime = oldDownTime
      latestDownTime['endTime'] = now.strftime("%Y-%m-%d %H:%M:%S")
      newDownTime.append(latestDownTime)
      slicer = min(20, len(newDownTime) - 1)
      newDownTime = newDownTime[-slicer:]
      status['downTime'] = newDownTime
  else:
    status['remark'] = "DOWN"
    if len(oldDownTime) == 0 or oldDownTime[-1].get('endTime', None) != None:
      newDownTime = oldDownTime
      newDownTime.append({'startTime': now.strftime("%Y-%m-%d %H:%M:%S")})
      slicer = min(20, len(newDownTime) - 1)
      newDownTime = newDownTime[-slicer:]
      status['downTime'] = newDownTime
    coloredPrint("DOWN: " + status['link'], RED)
  return status


def cronCall():
  oldStatus = []
  services = []
  statusAll = []
  try:
    with open('status.json') as json_file:
      oldStatus = json.load(json_file)['services']
  except:
    print("issue with loading old status, assuming no status")
  with open('services.json') as json_file:
    services = json.load(json_file)['services']

  num_threads = min(4, len(services))

  with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(
      checkStatus, {'service': service, 'downTime': next((x.get('downTime', []) for x in oldStatus if x['name'] == service['dns']), [])}) for service in services]
    concurrent.futures.wait(futures)
    statusAll = [future.result() for future in futures]

    coloredPrint("\n scanned all websites at " +
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " \n", BLUE)

  with open('status.json', 'w') as outfile:
    json.dump({"services": statusAll}, outfile, indent=2)


# cronCall()
