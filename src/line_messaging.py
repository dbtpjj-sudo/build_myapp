import requests

CHANNEL_ACCESS_TOKEN = "t+/NX3IteU1QBkLMqyJ+0S0ccceh00ER6EiDqYRGwcsCncZcQJjUjh0FprVi9MqfQ2LedG6PdoO9hgken975zUX5QWVe/NAcdrNiUrxtOHjARXQyAdrotYPY+0j6oB4KNnzOpmLpI6hxln/Q7aIEhwdB04t89/1O/w1cDnyilFU="

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