from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
import os
import asyncio

# Загружаем токен из .env или напрямую
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Flask-приложение
app = Flask(__name__)

# Пример API: корень
@app.route("/")
def index():
    return "Server and bot are running!"

# Пример API: приём бронирования
@app.route("/booking", methods=["POST"])
def booking():
    data = request.json
    print("Booking received:", data)
    # Здесь можно сохранить в базу, отправить админу и т.д.
    return jsonify({"status": "ok"})

# Telegram-бот
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот UnrealPlace 👾")

async def echo(update: Update, context):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def start_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Telegram bot is running...")
    app_bot.run_polling()

# Запускаем и Flask, и Telegram-бота параллельно
if __name__ == "__main__":
    import threading

    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
