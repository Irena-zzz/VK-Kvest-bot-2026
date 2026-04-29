import json
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

# 🔐 Твои данные
CONFIRMATION_CODE = "05b07636"
GROUP_TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn41lMK0gT3n7-1lbedKDmdjrSe-90ZGbwfGToCYM39V0dsZN3xB0E7IiH3p084Yp2f1Fn308fZ5N2xFhomSvF97k8DxxXqwksbUpnTKQSv6DvosUqaWwkCqUMIQTFDfkg8BCumwpCyoQ"
SECRET_KEY = "23i12r19i72n"
VK_API = "https://api.vk.com/method"

def send_message(peer_id, text):
    try:
        requests.post(f"{VK_API}/messages.send", {
            "peer_id": peer_id,
            "message": text,
            "random_id": 0,
            "access_token": GROUP_TOKEN,
            "v": "5.199"
        }, timeout=5)
    except:
        pass

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
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
                    send_message(peer_id, "Привет! Я работаю! 🚀")
                elif "как дела" in text:
                    send_message(peer_id, "Всё отлично!")
                else:
                    send_message(peer_id, "Напиши 'привет'.")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Отключаем логирование

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Bot running on port {port}")
    server.serve_forever()
