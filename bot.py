from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен бота
TOKEN = "7602590385:AAHGMNyQGuNrQeJi8h2Ht-n0OMbMKEyt9zU"

# URL Webhook Render
WEBHOOK_URL = "https://srv-crq0m4l6l47c73arhegg.onrender.com"

# Функция, которая отвечает на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает на Webhook.")

# Основная функция для запуска бота
def main():
    # Инициализация бота с токеном
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Настраиваем Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path=f"{TOKEN}",
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
