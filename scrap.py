import json
import os
from dotenv import load_dotenv
load_dotenv()


def scrap():
  services = []
  files = os.listdir(os.environ["NGINX_CONF_PATH"])

  for file in files:
    ser = {'dns': "", 'port': ""}
    with open("nginx-sites-enabled/" + file) as f:
      for line in f:
        if "server_name" in line:
          ser['dns'] = line.replace("server_name", "").replace(
            ".iitmandi.co.in;", "").strip()
        if "proxy_pass" in line:
          ser['port'] = line.split(":")[-1].replace(";", "").strip()
      services.append(ser)

  services = [{"dns": x["dns"], "port": int(
    x["port"])} for x in services if x['port'].isnumeric()]
  services.sort(key=lambda x: x['port'])

  with open("services.json", "w") as f:
    json.dump({'services': services}, f, indent=2)


# scrap()
