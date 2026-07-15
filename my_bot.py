import telebot
from telebot import types
import os
import threading
import time
import requests
from flask import Flask

# ========== ТВОИ НАСТРОЙКИ ==========
TOKEN = os.environ.get("BOT_TOKEN")
YOUR_TELEGRAM_ID = 5029046232
# =====================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ========== АВТО-ОЗДОРОВИТЕЛЬ ==========
def auto_healer():
    while True:
        time.sleep(3600)
        try:
            response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
            if response.status_code != 200:
                time.sleep(5)
                requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
        except:
            pass

threading.Thread(target=auto_healer, daemon=True).start()
# =========================================

# ========== ЗАЩИТА ОТ ЗАСЫПАНИЯ ==========
def keep_alive():
    while True:
        time.sleep(600)
        try:
            requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
        except:
            pass

threading.Thread(target=keep_alive, daemon=True).start()
# =========================================

WELCOME_TEXT = """🐾 Привет, осознанный собачник!

Я — клуб «Четыре Лапы Гурмана». Меня создала Ариана — профессиональный повар и хозяйка привередливой чихуахуа Мэгги. 🐶❤️

Я здесь, чтобы ты кормил своего питомца вкусно, безопасно и с любовью. Больше не нужно гуглить в панике «можно ли собаке огурец». 🥒

Вот что я умею:"""

CHECK_TEXT = "🐾 Давай знакомиться! Напиши кличку своего питомца, его породу, возраст и вес. А потом — какой продукт хочешь проверить. Например: «Бублик, мопс, 3 года, 8 кг, яблоко»."
MISKA_TEXT = "🥣 Напиши, пожалуйста, породу, вес и особенности твоего питомца (например, аллергии или чувствительный желудок). Например: «Мопс, 8 кг, аллергия на курицу». Я подберу безопасный ужин вручную."

CLUB_TEXT = """👩‍🍳 **Четыре Лапы Гурмана Премиум** — это наш закрытый клуб для тех, кто хочет баловать питомца по-особенному.

Внутри тебя ждут только эксклюзивные вещи, которых нет в бесплатной версии:
🍪 Эксклюзивные рецепты — личная коллекция Арианы для Мэгги, только для своих
❤️ Ежедневная «Лапка дня» — тёплое послание для тебя
🔮 Кулинарный гороскоп твоего питомца
💬 Живое общение и поддержка — возможность задать вопрос лично мне и получить ответ

Всё это — по платной подписке.
Напиши «Хочу в клуб», и я пришлю реквизиты. Сразу после оплаты ты получишь ссылку на наш закрытый канал «Четыре лапы Премиум». Первые 20 участников — по специальной цене. 🐶❤️"""

ASK_TEXT = "💬 Просто напиши свой вопрос прямо здесь, и Ариана ответит тебе лично. Я читаю все сообщения и рада помочь каждому хвостику."

ABOUT_TEXT = """🐾 О клубе «Четыре Лапы Гурмана»

Наш клуб родился из любви — к еде, к собакам и к осознанной заботе.

Меня зовут Ариана. Я пекарь, кондитер и хозяйка привередливой чихуахуа Мэгги. Однажды я поймала себя на том, что панически гуглю «можно ли собаке огурец»🥒 в три часа ночи. И поняла: миллионы людей хотят кормить своих питомцев вкусно и безопасно, но тонут в море противоречивой информации.

Наша миссия — сделать путь к натуральному питанию спокойным, радостным и научно обоснованным. Чтобы каждая миска была актом любви, а не тревоги.

Мы верим:
✨ Что осознанное питание — это не мода, а способ сказать питомцу «ты — часть семьи».
✨ Что забота должна быть доступной, понятной и красивой.
✨ Что каждый питомец уникален, и его рацион — тоже.

Что внутри клуба:
🦴 Персональная проверка продуктов с учётом породы, веса и аллергий
🥣 Конструктор безопасных мисок
👩‍🍳 Эксклюзивные рецепты от Шефа (личная коллекция Арианы для Мэгги)
❤️ «Лапка дня» — тёплое послание для тебя
🔮 Кулинарный гороскоп твоего питомца
💬 Живое общение и поддержка

А ещё я мечтаю создать приложение, которое будет доступно в AppStore, Play Market и RuStore — чтобы каждый хвостик в мире мог питаться правильно и безопасно.

Добро пожаловать в клуб. Мы тебе рады. 🐶❤️"""

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("🦴 Проверить продукт"),
        types.KeyboardButton("🥣 Собрать миску"),
        types.KeyboardButton("👩‍🍳 Лакомства от Шефа"),
        types.KeyboardButton("💬 Спросить Ариану"),
        types.KeyboardButton("🐾 О клубе")
    )
    return keyboard

# ========== ВЕБ-ЧАСТЬ ==========
@app.route('/')
def home():
    return "Bot is running!"

# ========== БОТ-ЧАСТЬ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    photo_url = "https://i.postimg.cc/qvmR3JgW/Artguru-20260713213826-artguru-(1).png"
    bot.send_photo(message.chat.id, photo_url, caption=WELCOME_TEXT, reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🦴 Проверить продукт")
def check_product(message):
    bot.send_message(message.chat.id, CHECK_TEXT)

@bot.message_handler(func=lambda m: m.text == "🥣 Собрать миску")
def make_bowl(message):
    bot.send_message(message.chat.id, MISKA_TEXT)

@bot.message_handler(func=lambda m: m.text == "👩‍🍳 Лакомства от Шефа")
def chef_treats(message):
    bot.send_message(message.chat.id, CLUB_TEXT)

@bot.message_handler(func=lambda m: m.text == "💬 Спросить Ариану")
def ask_ariana(message):
    bot.send_message(message.chat.id, ASK_TEXT)

@bot.message_handler(func=lambda m: m.text == "🐾 О клубе")
def about_club(message):
    bot.send_message(message.chat.id, ABOUT_TEXT)

@bot.message_handler(func=lambda m: True)
def forward_to_you(message):
    user_info = f"📩 Сообщение от @{message.from_user.username or 'без ника'} (ID: {message.from_user.id}):\n\n{message.text}"
    bot.send_message(YOUR_TELEGRAM_ID, user_info)
    bot.reply_to(message, "Спасибо! Ариана получила твой вопрос и скоро ответит ❤️")

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        app.run(host="0.0.0.0", port=10000)
    else:
        threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 10000}, daemon=True).start()
        bot.infinity_polling()
