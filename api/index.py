import os
import requests
import hmac
import hashlib

# 🔐 ВСТАВЬ СВОИ ДАННЫЕ НИЖЕ (между кавычками)
CONFIRMATION_CODE = "05b07636"      # ← сюда строку подтверждения
GROUP_TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-l1bedKDmdjrSe-9OZGbwfGToCYM39VOdsZN3xB0E7IiH3p084Yp2flFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQSv6DvosUqaWwkCqUMIQTDFkg8BCumwpCyoQ"            # ← сюда токен сообщества
SECRET_KEY = "23i12r19i72n"           # ← сюда секретный ключ

VK_API = "https://api.vk.com/method"

def send_message(peer_id, text):
    requests.post(f"{VK_API}/messages.send", {
        "peer_id": peer_id,
        "message": text,
        "random_id": 0,
        "access_token": G… # 2. Сообщение
    if event_type == 'message_new':
        msg = body['object']['message']
        peer_id = msg['peer_id']
        text = msg.get('text', '').lower()

        if 'привет' in text:
            send_message(peer_id, 'Привет! Я работаю на Yandex Cloud ☁️')
        elif 'как дела' in text:
            send_message(peer_id, 'Всё отлично!')
        else:
            send_message(peer_id, 'Я пока умею только здороваться. Напиши "привет".')

    return {'statusCode': 200, 'body': 'ok'}
