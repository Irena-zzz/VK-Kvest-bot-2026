
import os
import time
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from flask import Flask, request, jsonify

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

# Константы из вашего изображения
SECRET_KEY = "23i12r19i72n"
VALIDATION_STRING = "05b07636"
VK_TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-1lbedKDmdjrSe-9OZGbwfGToCYM3V9OdsZN3xB0E7lH3p084Yp2ffFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQsv6DvosUqaWwkCqUMIQTDfkg8BCumwpCyoQ"

# Flask endpoint для подтверждения сервера (Callback API)
@app.route('/vk_webhook', methods=['GET', 'POST'])
def vk_webhook():
    """
    Обработчик webhook от VK.
    VK отправляет secret ключ для подтверждения владения сервером.
    """
    if request.method == 'GET':
        # VK отправляет параметр secret для проверки
        received_secret = request.args.get('secret', '')
        logging.info(f"Получен secret для проверки: {received_secret}")
        
        if received_secret == SECRET_KEY:
            logging.info("✅ Secret совпадает! Возвращаем строку подтверждения.")
            return VALIDATION_STRING, 200
        else:
            logging.warning("❌ Secret не совпадает!")
            return 'Unauthorized', 401
    
    elif request.method == 'POST':
        # Обработка входящих событий от VK (Callback API)
        data = request.json
        logging.info(f"Получено событие: {data.get('type', 'unknown')}")
        
        if data.get('type') == 'message_new':
            handle_new_message(data['object'])
        
        return 'ok', 200

def handle_new_message(message_obj):
    """Обработка нового сообщения"""
    try:
        vk = vk_api.VkApi(token=VK_TOKEN)
        peer_id = message_obj['message']['peer_id']
        text = message_obj['message']['text'].strip().lower()
        
        if text in ('привет', 'hi', 'здравствуй'):
            vk.method("messages.send", {
                "peer_id": peer_id,
                "message": "Привет! Я бот на Bothost 🚀",
                "random_id": int(time.time() * 1000)
            })
        elif text == 'помощь':
            vk.method("messages.send", {
                "peer_id": peer_id,
                "message": "Команды: привет, помощь, время",
                "random_id": int(time.time() * 1000)
            })
        elif text == 'время':
            current_time = time.strftime("%H:%M:%S", time.localtime())
            vk.method("messages.send", {
                "peer_id": peer_id,
                "message": f"Время: {current_time}",
                "random_id": int(time.time() * 1000)
            })
            
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

# Long Poll (альтернативный вариант, если не используете Callback API)
def run_longpoll_bot():
    """Запуск бота через Long Poll"""
    vk = vk_api.VkApi(token=VK_TOKEN)
    longpoll = VkBotLongPoll(vk)
    logging.info("✅ Бот запущен (Long Poll). Ожидаю сообщения...")
    
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                msg = event.obj['message']['text'].strip().lower()
                peer_id = event.obj['message']['peer_id']
                
                if msg in ('привет', 'hi'):
                    vk.method("messages.send", {
                        "peer_id": peer_id,
                        "message": "Привет! 🚀",
                        "random_id": int(time.time() * 1000)
                    })
                    
        except Exception as e:
            logging.error(f"Ошибка: {e}")

if __name__ == "__main__":
    # Для Bothost: запускаем Flask сервер для Callback API
    # Порт и хост берутся из переменных окружения Bothost
    port = int(os.getenv('PORT', 5000))
    logging.info(f"🚀 Запуск сервера на порту {port}")
    app.run(host='0.0.0.0', port=port)
    
    # ИЛИ для Long Poll (раскомментируйте, если используете Long Poll):
    # run_longpoll_bot()
