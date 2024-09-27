import logging
import feedparser
import random
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Прокси серверы
proxies = [
    "http://152.26.229.42:9443",
    "http://157.254.53.50:80",
]

# Функция для перевода текста
def translate_text(text, dest_lang):
    try:
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except Exception as e:
        return text  # В случае ошибки возвращаем оригинальный текст

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот AfghanMonitor и готов к работе.")

# Функция для получения и отправки новостей
async def fetch_and_send_news(context):
    chat_id = -1002308007225  # ваш chat_id канала
    rss_urls = [
        "https://www.albawaba.com/rss.xml",  # Al Bawaba RSS
        "https://www.annahar.com/rss",  # An-Nahar RSS
        "https://www.al-akhbar.com/feeds",  # Al Akhbar RSS
    ]

    # Ключевые слова на английском
    keywords = {
        'en': ["Afghanistan", "Taliban", "Baradar", "Haqqani", "Yakub", "Massoud", "Yasin Zia", "Dostum", "Ahundzada"],
    }

    sent_titles = set()  # Множество для хранения отправленных заголовков

    for rss_url in rss_urls:
        try:
            proxy = random.choice(proxies)  # Выбор случайного прокси
            logging.info(f"Using proxy: {proxy}")  # Лог для отслеживания прокси
            feed = feedparser.parse(rss_url, request_headers={"User-Agent": "Mozilla/5.0"}, proxies={"http": proxy, "https": proxy})

            if feed.bozo:  # Проверка на ошибки
                logging.error(f"Error parsing {rss_url}: {feed.bozo_exception}")
                continue

            for entry in feed.entries:
                title = entry.title
                logging.info(f"Checking title: {title}")  # Лог заголовка
                if title in sent_titles:
                    continue  # Пропустить, если заголовок уже отправлен

                # Проверка ключевых слов на английском
                if any(keyword.lower() in title.lower() for keyword in keywords['en']):
                    logging.info(f"Matched title: {title}")  # Лог для совпадения
                    link = entry.link
                    summary = entry.get('summary', '')
                    translated_title = translate_text(title, 'ru')
                    translated_summary = translate_text(summary, 'ru')
                    message = f"{translated_title}nn{translated_summary}n{link}"
                    await context.bot.send_message(chat_id=chat_id, text=message)
                    sent_titles.add(title)  # Добавить заголовок в множество отправленных

        except Exception as e:
            logger.error(f"Ошибка при обработке {rss_url}: {e}")

# Основная функция для запуска бота
def main():
    application = Application.builder().token("7602590385:AAHGMNyQGuNrQeJi8h2Ht-n0OMbMKEyt9zU").build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Настройка задачи для отправки новостей каждые 10 минут
    job_queue = application.job_queue
    job_queue.run_repeating(fetch_and_send_news, interval=600, first=10)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()

