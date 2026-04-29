mport json
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIRMATION_CODE = "05b07636"
GROUP_TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn41lMK0gT3n7-1lbedKDmdjrSe-90ZGbwfGToCYM39V0dsZN3xB0E7IiH3p084Yp2f1Fn308fZ5N2xFhomSvF97k8DxxXqwksbUpnTKQSv6DvosUqaWwkCqUMIQTFDfkg8BCumwpCyoQ"
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
    except Exception as e:
        print(f"Error sending message: {e}")

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length)
            body = json.loads(data)
            
            if body.get("type") == "confirmation":
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(CONFIRMATION_CODE.encode())
                return
            
            if body.get("type") == "message_new":
                msg = body["object"]["message"]
                peer_id = msg["peer_id"]
                text = msg.get("text", "").lower()
                
                if "привет" in text:
                    send_message(peer_id, "Привет! 🚀")
                else:
                    send_message(peer_id, "Напиши 'привет'")
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"{args}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Starting server on port {port}")
    server.serve_forever()
