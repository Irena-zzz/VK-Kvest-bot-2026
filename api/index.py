import json
import os
import requests

CONFIRMATION_CODE = os.environ.get('05b07636', 'test')
GROUP_TOKEN = os.environ.get('vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-l1bedKDmdjrSe-9OZGbwfGToCYM39VOdsZN3xB0E7IiH3p084Yp2flFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQSv6DvosUqaWwkCqUMIQTDFkg8BCumwpCyoQ')
SECRET_KEY = os.environ.get('23i12r19i72n')

VK_API = "https://api.vk.com/method"

def send_message(peer_id, text):
    requests.post(f"{VK_API}/messages.send", {
        "peer_id": peer_id,
        "message": text,
        "random_id": 0,
        "access_token": GROUP_TOKEN,
        "v": "5.199"
    })

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
    except:
        return {'statusCode': 400, 'body': 'Error'}

    event_type = body.get('type')

    if event_type == 'confirmation':
        return {'statusCode': 200, 'body': CONFIRMATION_CODE}

    if event_type == 'message_new':
        msg = body['object']['message']
        peer_id = msg['peer_id']
        text = msg.get('text', '').lower()

        if 'привет' in text:
            send_message(peer_id, 'Привет! Я работаю на Bothost!')
        elif 'как дела' in text:
            send_message(peer_id, 'Всё отлично!')
        else:
            send_message(peer_id, 'Напиши "привет"')

    return {'statusCode': 200, 'body': 'ok'}
