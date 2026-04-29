import asyncio
from vkbottle.bot import Bot, Message
# Замени на свой токен сообщества
TOKEN = "vk1.a.TTUwA_6B6ZWp-bZTn9AWUDt3UJxHjzEJ6oivPZ2Jc_AfdLk39xo2V_VIwSqiASAwrIkdlRZP3B0saOOFQuDquYO2eP3tAhRrcvIG26KtPi7CpJFNQoydvwK1LbBa82Tx3yUEpxjnmgW0oIYklKO2HL9X0xXoJk7JC0NLA9vCZppPErMlO4IBNW3tJ2-Nu9-CUwZ_N3TpkKx8YRClCJZctg"
bot = Bot(token=TOKEN)
@bot.on.message(text=["привет", "здравствуй", "хай", "hi", "hello"])
async def greet_handler(message: Message):
await message.answer("Привет! Я бот этого сообщества 🤖")
@bot.on.message(text=["что ты умеешь", "помощь", "/help"])
async def help_handler(message: Message):
await message.answer(
"Я умею:\n"
"• Отвечать на приветствия\n"
"• Рассказывать о себе\n"
"\nНапиши «привет» чтобы начать!"
)
@bot.on.message()
async def fallback_handler(message: Message):
await message.answer("Не понял тебя 🤔 Напиши «помощь» чтобы узнать что я умею.")
if __name__ == "__main__":
bot.run_forever()
