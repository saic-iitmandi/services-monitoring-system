# this has the function to send message to discord channel
import requests
import os
from dotenv import load_dotenv
load_dotenv()
#   "components": [
#     {
#       "type": 1,
#       "components": [
#         {
#           "style": 5,
#           "label": "Visit",
#           "url": "https://status.iitmandi.co.in/service/nirmaan",
#           "disabled": False,
#           "type": 2
#         },
#         {
#           "style": 5,
#           "label": "Status",
#           "url": "https://status.iitmandi.co.in/service/nirmaan",
#           "disabled": False,
#           "type": 2
#         }
#       ]
#     }
#   ],


def webhook(inpType, inp):
  url = os.environ.get("WEBHOOK_URL")
  if inpType == "down":
    down = {
      "content": "ALERT!!!",
      "tts": False,

      "embeds": [
          {
              "type": "rich",
              "title": inp["name"] + " DOWN",
              "description": "",
              "color": 0xff2a00,
              "fields": [
                  {
                      "name": "port:",
                      "value": inp["port"],
                      "inline": True
                  },
                  {
                      "name": "dns:",
                      "value": inp["dns"]
                  },
                  {
                      "name": "Remark",
                      "value": "DOWN"
                  }
              ],
              "url": "https://status.iitmandi.co.in/service/" + inp["name"]
          }
      ]
        }
    data = down
  elif inpType == "up":
    up = {
      "content": "ALERT!!!",
      "tts": False,

      "embeds": [
          {
              "type": "rich",
              "title": inp["name"] + " UP AGAIN",
              "description": "",
              "color": 0x40ff00,
              "fields": [
                  {
                      "name": "port:",
                      "value": inp["port"],
                      "inline": True
                  },
                  {
                      "name": "dns:",
                      "value": inp["dns"]
                  },
                  {
                      "name": "Remark",
                      "value": "UP AGAIN"
                  }
              ],
              "url": "https://status.iitmandi.co.in/service/" + inp["name"]
          }
      ]
        }
    data = up
  elif inpType == "ticket":
    ticket = {
      "content": "TICKET",
      "tts": False,
      "embeds": [
          {
              "type": "rich",
              "title": inp["title"],
              "description": inp["content"],
              "color": 0x00FFFF,
              "fields": [
                  {
                      "name": "from",
                      "value": inp["email"]
                  }
              ]
          }
      ]
        }
    data = ticket

  result = requests.post(url, json=data)

  try:
    result.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(err)
  else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
    if "template" in data:
      print("Template: {}".format(data["template"]))
