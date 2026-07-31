import requests

CHANNEL_ACCESS_TOKEN = "q3N6Vo8s29iHv8b+YA2pFq0im8KjHlePLQBIHsbRo7H6Yt/ThqwHXo+FvWc/+FF5Q2LedG6PdoO9hgken975zUX5QWVe/NAcdrNiUrxtOHgSfMPlIqtd3Opg5OqpXFDHySdu4/Jozm2l+N4rPi5FJQdB04t89/1O/w1cDnyilFU="
USER_ID = "U0c5cc0c78114ecdd3daea584f4d22dbf"

def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    r = requests.post(url, headers=headers, json=body)

    print("LINE STATUS:", r.status_code)
    print(r.text)