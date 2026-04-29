import json
import requests
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# 🔐 Твои данные
CONFIRMATION_CODE = "05b07636"
GROUP_TOKEN = "vk1.a.vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-l1bedKDmdjrSe-9OZGbwfGToCYM39VOdsZN3xB0E7IiH3p084Yp2flFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQSv6DvosUqaWwkCqUMIQTDFkg8BCumwpCyoQ"
SECRET_KEY = "23i12r19i72n"
VK_API = "https://api.vk.com/method"

def send_message(peer_id, text):
    requests.post(f"{VK_API}/messages.send", {
        "peer_id": peer_id,
        "message": text,
        "random_id": 0,
        "access_token": GROUP_TOKEN,
        "v": "5.199"
    })

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)
        
        event_type = body.get("type")
        
        # 1. Подтверждение сервера
        if event_type == "confirmation":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(CONFIRMATION_CODE.encode())
            return

        # 2. Сообщение
        if event_type == "message_new":
            msg = body["object"]["message"]
            peer_id = msg["peer_id"]
            text = msg.get("text", "").lower()
            
            if "привет" in text:
                send_message(peer_id, "Привет! Я работаю на Bothost! 🚀")
            elif "как дела" in text:
                send_message(peer_id, "Всё отлично!")
            else:
                send_message(peer_id, "Напиши 'привет'.")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"Bot running on port {port}")
    server.serve_forever()
