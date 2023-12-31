import json


def getAllServices():
  servicesStatus = []
  try:
    with open('status.json') as json_file:
      servicesStatus = json.load(json_file)['services']
      return [{k: v for k, v in service.items() if k != 'port'} for service in servicesStatus]
  except FileNotFoundError:
    # also call the cron function
    with open('status.json', 'w') as f:
      json.dump({"services": []}, f)
  except:
    print('err')
    return None
  return servicesStatus


def getService(name):
  servicesStatus = getAllServices()
  if servicesStatus == None:
    return None
  return next((x for x in servicesStatus if x['dns'] == name), None)
