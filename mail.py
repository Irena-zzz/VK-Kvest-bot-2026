import os
import time
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    # Получаем токен из ENV или используем токен по умолчанию
    token = os.getenv("VK_GROUP_TOKEN") or "vk1.a.CkPgupAiYsZNaeUMoopB1SzXeShDo2gndVLxtiWSvJ1LZ5-X3aXw_-YyrCyCtAD6aPwzJMmkZXDFn4lMK0gT3n7-1lbedKDmdjrSe-9OZGbwfGToCYM3V9OdsZN3xB0E7lH3p084Yp2ffFn308fZ5N2xFhomSvF97k8DxxXqwkbsUPnTKQsv6DvosUqaWwkCqUMIQTDfkg8BCumwpCyoQ"
    
    if not token or token.startswith("vk1."):
        logging.info("✅ Токен получен")
    else:
        logging.error("❌ Токен недействителен!")
        return

    # Инициализация VK API и Long Poll
    vk = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk)
    logging.info("✅ Бот запущен. Ожидаю сообщения...")

    # Основной цикл событий
    for event in longpoll.listen():
        try:
            if event.type != VkBotEventType.MESSAGE_NEW or not event.from_user:
                continue

            msg = event.obj['message']['text'].strip().lower()
            peer_id = event.obj['message']['peer_id']

            if msg in ("привет", "hi", "здравствуй"):
                vk.method("messages.send", {
                    "peer_id": peer_id,
                    "message": "Привет! Я бот, работающий на Bothost 🚀",
                    "random_id": int(time.time() * 1000)
                })
            elif msg == "помощь":
                vk.method("messages.send", {
                    "peer_id": peer_id,
                    "message": "Доступные команды:\n• привет\n• помощь\n• время",
                    "random_id": int(time.time() * 1000)
                })
            elif msg == "время":
                current_time = time.strftime("%H:%M:%S", time.localtime())
                vk.method("messages.send", {
                    "peer_id": peer_id,
                    "message": f"Текущее время: {current_time}",
                    "random_id": int(time.time() * 1000)
                })

        except vk_api.exceptions.ApiError as e:
            logging.warning(f"⚠️ Ошибка VK API: {e}")
        except Exception as e:
            logging.error(f"💥 Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
