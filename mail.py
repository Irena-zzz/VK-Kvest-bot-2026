import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time

# Ваш токен
TOKEN = "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-1lbedKDmdjrSe-9OZGbwfGToCYM3V9OdsZN3xB0E7lH3p084Yp2ffFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQsv6DvosUqaWwkCqUMIQTDfkg8BCumwpCyoQ"

print("🚀 Запуск бота...")

# Авторизация
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session)

print("✅ Бот запущен и готов к работе!")

# Бесконечный цикл
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
        message_text = event.obj['message']['text'].lower().strip()
        user_id = event.obj['message']['from_id']
        
        print(f"📩 Сообщение от {user_id}: {message_text}")
        
        # Ответы на команды
        if message_text in ['привет', 'hi', 'здравствуй']:
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': 'Привет! Я работаю! 👋',
                'random_id': int(time.time() * 1000)
            })
            print(f"✅ Ответ отправлен пользователю {user_id}")
            
        elif message_text == 'помощь':
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': 'Команды:\n- привет\n- помощь\n- время',
                'random_id': int(time.time() * 1000)
            })
            
        elif message_text == 'время':
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': f'Сейчас {now}',
                'random_id': int(time.time() * 1000)
            })
