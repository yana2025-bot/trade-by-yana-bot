import os
import telebot
from datetime import datetime
import random

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Привіт! Я бот для торгівлі валютною парою EUR/USD.\n"
                                      "Натисни кнопку нижче, щоб отримати сигнал 📈",
                     reply_markup=main_menu())

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📈 Отримати сигнал")
    return markup

@bot.message_handler(func=lambda message: message.text == "📈 Отримати сигнал")
def handle_signal(message):
    now = datetime.now()
    minutes = now.minute

    if minutes % 2 == 0:
        direction = "⬆️ ВГОРУ" if random.random() > 0.5 else "⬇️ ВНИЗ"
        bot.send_message(message.chat.id,
            f"✅ Готовий сигнал:\n"
            f"🔹 Актив: EUR/USD\n"
            f"🔹 Напрямок: {direction}\n"
            f"🔹 Час угоди: 4 хвилини\n"
            f"🔹 Ймовірність: 70–90%")
    else:
        bot.send_message(message.chat.id, "⏳ Зараз немає сильного сигналу. Спробуй через 1–2 хвилини.")

bot.polling()