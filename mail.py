from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# 🔐 Твои данные
CONFIRMATION = "1425493f"
TOKEN = "vk1.a.TTUwA_6B6ZWp-bZTn9AWUDt3UJxHjzEJ6oivPZ2Jc_AfdLk39xo2V_VIwSqiASAwrIkdlRZP3B0saOOFQuDquYO2eP3tAhRrcvIG26KtPi7CpJFNQoydvwK1LbBa82Tx3yUEpxjnmgW0oIYklKO2HL9X0xXoJk7JC0NLA9vCZppPErMlO4IBNW3tJ2-Nu9-CUwZ_N3TpkKx8YRClCJZctg"

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('type')
    
    # Подтверждение
    if event == 'confirmation':
        return Response(CONFIRMATION, status=200, mimetype='text/plain')
    
    # Сообщение
    if event == 'message_new':
        msg = data['object']['message']
        peer_id = msg['peer_id']
        text = msg.get('text', '').lower()
        
        if 'привет' in text:
            send_msg(peer_id, 'Привет! Я работаю! 🚀')
        else:
            send_msg(peer_id, 'Напиши "привет"')
    
    return 'ok', 200

def send_msg(peer_id, text):
    try:
        requests.post('https://api.vk.com/method/messages.send', {
            'peer_id': peer_id,
            'message': text,
            'random_id': 0,
            'access_token': TOKEN,
            'v': '5.199'
        }, timeout=5)
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
