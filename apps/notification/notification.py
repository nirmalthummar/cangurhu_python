import json

import requests

from cangurhu.settings import FIREBASE_SERVER_KEY


def send_notification(user_device_tokens, message_title, message_desc):
    try:
        fcm_api = FIREBASE_SERVER_KEY
        url = "https://fcm.googleapis.com/fcm/send"

        headers = {
            "Content-Type": "application/json",
            "Authorization": 'key=' + fcm_api}

        payload = {
            "registration_ids": user_device_tokens,
            "priority": "high",
            "notification": {
                "body": message_desc,
                "title": message_title,
            }

        }
        result = requests.post(url, data=json.dumps(payload), headers=headers)
        print(result.json())
    except Exception as e:
        print(e)
