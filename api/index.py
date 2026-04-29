import json
from fastapi import FastAPI, Request, Response
import os
import requests

app = FastAPI()

# 🔐 ВСТАВЬ СВОИ ДАННЫЕ НИЖЕ (между кавычками)
CONFIRMATION_CODE = "05b07636"      # ← сюда строку подтверждения
GROUP_TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-l1bedKDmdjrSe-9OZGbwfGToCYM39VOdsZN3xB0E7IiH3p084Yp2flFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQSv6DvosUqaWwkCqUMIQTDFkg8BCumwpCyoQ"            # ← сюда токен сообщества
SECRET_KEY = "23i12r19i72n"           # ← сюда секретный ключ

VK_API = "https://api.vk.com/method"

def send_message(peer_id: int, text: str):
    requests.post(f"{VK_API}/messages.send", {
        "peer_id": peer_id,
        "message": text,
        "random_id": 0,
        "access_token": GROUP_TOKEN,
        "v": "5.199"
    })

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    event_type = data.get("type")

    # 1. Подтверждение сервера
    if event_type == "confirmation":
        return Response(content=CONFIRMATION_CODE, media_type="text/plain")

    # 2. Входящее сообщение
    if event_type == "message_new":
        msg = data["object"]["message"]
        peer_id = msg["peer_id"]
        text = msg.get("text", "").lower()

        if "привет" in text:
            send_message(peer_id, "Привет! Я работаю на Vercel 🚀")
        elif "как дела" in text:
            send_message(peer_id, "Всё отлично! Напиши 'привет'")
        else:
            send_message(peer_id, "Напиши 'привет' или 'как дела'")

    return Response(status_code=200)
