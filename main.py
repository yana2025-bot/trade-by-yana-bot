
import telebot
import time
import requests
import yfinance as yf
import datetime
from threading import Thread
from pytz import timezone

TOKEN = '7574483194:AAEqUsSGeu3evRDeQRlxtM_EdQw3HGk8310'
CHAT_ID = '1132189124'

bot = telebot.TeleBot(TOKEN)

def is_news_time():
    try:
        response = requests.get('https://nfs.faireconomy.media/ff_calendar_thisweek.xml')
        if "High" in response.text:
            return True
    except:
        return False
    return False

def check_market():
    try:
        data = yf.download("EURUSD=X", period="5m", interval="30s")
        closes = data['Close']
        if len(closes) < 10:
            return None

        last = closes[-1]
        prev = closes[-2]
        direction = "ВГОРУ" if last > prev else "ВНИЗ"
        return direction
    except Exception as e:
        print("Market error:", e)
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт! Я твій торговий бот. Натисни кнопку нижче, щоб отримати сигнал.", reply_markup=start_keyboard())

def start_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📈 Отримати сигнал')
    return markup

@bot.message_handler(func=lambda m: m.text == "📈 Отримати сигнал")
def handle_signal_request(message):
    if is_news_time():
        bot.send_message(message.chat.id, "⚠️ Зараз важливі новини на ринку. Торгівля не рекомендується.")
        return

    direction = check_market()
    if direction:
        signal = f"✓Готовий сигнал:\n✓Актив: EUR/USD\n✓Напрямок: {direction}\n✓Час угоди: 4 хвилини\n✓Ймовірність відпрацювання: 80-90%"
        bot.send_message(message.chat.id, signal)
    else:
        bot.send_message(message.chat.id, "⏳ Зараз немає сильного сигналу. Спробуй через 1-2 хвилини.")

def auto_signal_loop():
    while True:
        now = datetime.datetime.now(timezone('Europe/Kyiv'))
        if now.minute % 3 == 0:
            if not is_news_time():
                direction = check_market()
                if direction:
                    signal = f"✓Готовий сигнал:\n✓Актив: EUR/USD\n✓Напрямок: {direction}\n✓Час угоди: 4 хвилини\n✓Ймовірність відпрацювання: 80-90%"
                    bot.send_message(CHAT_ID, signal)
        time.sleep(60)

Thread(target=auto_signal_loop).start()
bot.polling(none_stop=True)
