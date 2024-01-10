# this has the function to send message to discord channel
import requests 
import os

data = {
    "content" : "Website Status",
    "username" : "Bot",
    "template": {
    "field1": "value1",
    "field2": "value2",
    }
}

def webhook(data):
    url = os.environ.get("WEBHOOK_URL")
    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))
        if "template" in data:
            print("Template: {}".format(data["template"]))

webhook(data)