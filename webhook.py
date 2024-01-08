import requests 

data = {
    "content" : "Website Status",
    "username" : "Bot",
    "template": {
    "field1": "value1",
    "field2": "value2",
    }
}

def webhook(data):
    url = "https://discord.com/api/webhooks/1192917462052786307/TIx4Vk-auZzW8a4QFaUUxez7AM37OpfGA05uMH_yirRwWLbWZGi6JsW0_BaLx-xcBBq5" #webhook url, from here: https://i.imgur.com/f9XnAew.png
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