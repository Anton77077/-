from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен бота
TOKEN = "7602590385:AAHGMNyQGuNrQeJi8h2Ht-n0OMbMKEyt9zU"

# Функция, которая отвечает на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает.")

# Основная функция для запуска бота
def main():
    # Инициализация бота с токеном
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
