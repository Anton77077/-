import feedparser
import requests
from deep_translator import GoogleTranslator
from telegram import Bot
from telegram.ext import Application, CommandHandler, JobQueue
import random

# Прокси серверы
proxies = [
    "http://152.26.229.42:9443",
    "http://157.254.53.50:80",
    "socks4://95.111.227.164:39556",
    # Добавьте больше прокси из списка
]

# Функция для перевода текста
def translate_text(text, dest_lang):
    try:
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except Exception as e:
        return text  # В случае ошибки возвращаем оригинальный текст

# Функция для обработки команды /start
async def start(update, context):
    await update.message.reply_text("Привет! Я бот AfghanMonitor и готов к работе. Я буду публиковать новости о Афганистане.")

# Функция для получения и отправки новостей
async def fetch_and_send_news(context):
    chat_id = -1002308007225  # ваш chat_id канала
# RSS-источники по разным языкам
    rss_urls = [
    # Английский
    "https://feeds.bbci.co.uk/news/world/rss.xml",  # BBC World News RSS
    "https://www.aljazeera.com/xml/rss/all.xml",  # Al Jazeera RSS
    "https://feeds.reuters.com/reuters/topNews",  # Reuters RSS
    "https://www.theguardian.com/world/rss",  # The Guardian World News RSS
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",  # The New York Times RSS
    "http://rss.cnn.com/rss/edition_world.rss",  # CNN RSS
    "https://foreignpolicy.com/feed/",  # Foreign Policy RSS
    "https://www.politico.com/rss/politics.xml",  # Politico RSS
    "http://feeds.nbcnews.com/feeds/world",  # NBC News RSS
    "https://asiatimes.com/feed/",  # Asia Times RSS

    # Французский
    "https://www.lemonde.fr/rss/une.xml",  # Le Monde RSS
    "https://www.france24.com/en/rss",  # France 24 RSS
    "https://www.rfi.fr/rss",  # RFI RSS
    "https://www.lefigaro.fr/rss/figaro_international.xml",  # Le Figaro RSS
    "https://www.nouvelobs.com/rss.xml",  # L'Obs RSS
    "https://www.liberation.fr/rss",  # Libération RSS
    "https://www.courrierinternational.com/rss.xml",  # Courrier International RSS
    "https://www.mediapart.fr/feed",  # Mediapart RSS
    "https://www.la-croix.com/rss",  # La Croix RSS
    "https://www.lesechos.fr/rss",  # Les Echos RSS

    # Немецкий
    "https://rss.dw.com/rdf/rss-en-all",  # DW RSS
    "https://www.faz.net/rss/aktuell/",  # FAZ RSS
    "https://newsfeed.zeit.de/index",  # Die Zeit RSS
    "https://www.sueddeutsche.de/app/service/rss/alles/rss.xml",  # Süddeutsche Zeitung RSS
    "https://www.spiegel.de/international/index.rss",  # Der Spiegel RSS
    "https://www.handelsblatt.com/rss",  # Handelsblatt RSS
    "https://www.tagesschau.de/xml/rss2",  # Tagesschau RSS
    "https://taz.de/!p4608;rss/",  # taz RSS
    "https://www.welt.de/feeds/section/politik.rss",  # Welt RSS
    "https://www.nzz.ch/feed/nzz/de/rss",  # NZZ RSS

    # Арабский
    "https://www.aljazeera.net/aljazeera/rss",  # Al Jazeera Arabic RSS
    "https://www.alarabiya.net/ar/tools/rss.html",  # Al Arabiya RSS
    "https://aawsat.com/rss.xml",  # Asharq Al-Awsat RSS
    "https://www.alquds.co.uk/feed/",  # Al Quds RSS
    "https://www.al-monitor.com/rss",  # Al-Monitor RSS
    "https://www.middleeasteye.net/rss.xml",  # Middle East Eye RSS
    "https://www.albawaba.com/rss.xml",  # Al Bawaba RSS
    "https://www.annahar.com/rss",  # An-Nahar RSS
    "https://www.al-akhbar.com/feeds",  # Al Akhbar RSS
    "https://www.raialyoum.com/index.php/feed/",  # Rai Al Youm RSS

    # Персидский
    "https://www.bbc.com/persian/rss.xml",  # BBC Persian RSS
    "https://www.radiofarda.com/rss",  # Radio Farda RSS
    "https://rss.dw.com/rss-per-all",  # DW Persian RSS
    "https://iranintl.com/rss",  # Iran International RSS
    "https://www.tasnimnews.com/en/rss/feed",  # Tasnim News RSS
    "https://www.farsnews.ir/en/rss",  # Fars News RSS
    "https://www.etemadonline.com/rss",  # Etemad Online RSS
    "https://www.sharghdaily.com/rss",  # Shargh Daily RSS
    "https://kayhan.ir/fa/rss",  # Kayhan RSS
    "https://www.asriran.com/fa/rss/allnews",  # Asr-e Iran RSS

    # Пушту
    "https://www.voadeewanews.com/rss",  # VOA Pashto RSS
    "https://www.azadiradio.com/api/zkgqoehr$oqv",  # Azadi Radio Pashto RSS
    "https://www.bbc.co.uk/pashto/rss.xml",  # BBC Pashto RSS
    "https://www.tolonews.com/rss",  # Tolo News Pashto RSS
    "https://www.khybernews.tv/feed/",  # Khyber News RSS
    "https://www.mashaalradio.com/api/zr$ope-$ip",  # Mashaal Radio Pashto RSS

    # Турецкий
    "https://www.aa.com.tr/en/rss",  # Anadolu Agency RSS
    "https://www.hurriyetdailynews.com/rss",  # Hürriyet RSS
    "https://www.milliyet.com.tr/rss/rss.xml",  # Milliyet RSS
    "https://www.sabah.com.tr/rss.xml",  # Sabah RSS
    "https://www.cumhuriyet.com.tr/rss.xml",  # Cumhuriyet RSS
    "https://www.trthaber.com/en/rss",  # TRT Haber RSS
    "https://www.yenisafak.com/rss",  # Yeni Şafak RSS
    "https://www.sozcu.com.tr/rss",  # Sözcü RSS
    "https://www.haberturk.com/rss",  # Habertürk RSS
    "https://www.dunya.com/feed",  # Dünya RSS

    # Пакистанские СМИ
    "https://www.dawn.com/rss",  # Dawn RSS
    "https://tribune.com.pk/rss",  # The Express Tribune RSS
    "https://www.geo.tv/rss/1/1",  # Geo News RSS
    "https://arynews.tv/rss/",  # ARY News RSS
    "https://nation.com.pk/rss",  # The Nation RSS
    "https://www.pakistantoday.com.pk/rss",  # Pakistan Today RSS
    "https://jang.com.pk/rss",  # Jang News RSS
    "https://www.thenews.com.pk/rss/1/1",  # The News International RSS
    "https://www.samaa.tv/rss",  # Samaa TV RSS
    "https://www.brecorder.com/rss",  # Business Recorder RSS

    # Китайский
    "http://www.xinhuanet.com/english/rss/china_news.rss",  # Xinhua RSS
    "https://www.globaltimes.cn/rss/china.xml",  # Global Times RSS
    "http://www.chinadaily.com.cn/rss/china_rss.xml",  # China Daily RSS
    "http://en.people.cn/rss/china.xml",  # People's Daily RSS
    "http://www.caixinglobal.com/rss.xml",  # Caixin Global RSS
    "https://www.scmp.com/rss/3/feed",  # SCMP RSS
    "https://www.yicaiglobal.com/news/rss",  # Yicai Global RSS

    # Индия
    "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms",  # The Times of India RSS
    "https://www.thehindu.com/feeder/default.rss",  # The Hindu RSS
    "https://www.ndtv.com/rss",  # NDTV RSS
    "https://www.hindustantimes.com/rss/topnews/rssfeed.xml",  # Hindustan Times RSS
    "https://www.indiatoday.in/rss/1206578",  # India Today RSS
    "https://indianexpress.com/section/world/feed/",  # Indian Express RSS
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",  # The Economic Times RSS
    "https://www.business-standard.com/rss",  # Business Standard RSS
    "https://theprint.in/feed/",  # The Print RSS
    "https://www.firstpost.com/rss/india.xml",  # Firstpost RSS

    # Таджикистан
    "https://asiaplustj.info/rss/",  # Asia-Plus RSS
    "https://khovar.tj/ru/rss",  # Khovar RSS (Национальное информационное агентство Таджикистана)
    "https://www.avesta.tj/rss",  # Avesta News Agency RSS
    "https://www.tajikta.tj/rss.xml",  # Tajikistan News (Tajik TAJ) RSS
    "https://www.ozodi.org/api/zp",  # Ozodi (Tajik service of Radio Free Europe/Radio Liberty) RSS
    "https://faraj.tj/rss",  # Faraj RSS
    "https://sugdnews.info/rss",  # SugdNews RSS
    "https://pressa.tj/feed",  # Pressa.tj RSS
    "https://asiaplustj.info/en/rss/",  # Asia-Plus Business RSS
]
    
    keywords = ["Afghanistan", "Taliban", "Baradar", "Haqqani", "Yakub", "Massoud", "Yasin Zia", "Dostum", "Ahundzada"]

    for rss_url in rss_urls:
        try:
            proxy = random.choice(proxies)
            proxies_dict = {"http": proxy, "https": proxy}
            feed = feedparser.parse(rss_url, request_headers={"User-Agent": "Mozilla/5.0"})
            for entry in feed.entries:
                if any(keyword.lower() in entry.title.lower() for keyword in keywords):
                    title = entry.title
                    link = entry.link
                    summary = entry.get('summary', '')
                    translated_title = translate_text(title, 'ru')
                    translated_summary = translate_text(summary, 'ru')
                    message = f"{translated_title}\n\n{translated_summary}\n{link}"
                    await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Ошибка при обработке {rss_url}: {e}")

# Основная функция для запуска бота
def main():
    application = Application.builder().token("7607087769:AAEv3ssr8hJ1Z_UaH6Sp19mKSrjQKWAP6rs").build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Настройка задачи для отправки новостей каждые 10 минут
    job_queue = application.job_queue
    job_queue.run_repeating(fetch_and_send_news, interval=600, first=10)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
