from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
from datetime import datetime
import pytz

# Данные для Telegram
CHAT_ID = "2110364647"
BOT_TOKEN = "8151764416:AAE0F-wPCFZDViO7b5BQV-q7YjBHz0n8izA"

# URL страницы стрима
URL = "https://www.donationalerts.com/r/amichkaplay"

# Часовой пояс Москвы
moscow_tz = pytz.timezone("Europe/Moscow")

def send_telegram_message(text):
    """Функция отправки сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
        print("Сообщение отправлено в Telegram.")
    except requests.RequestException as e:
        print(f"Ошибка отправки в Telegram: {e}")

def check_stream():
    """Функция проверки стрима"""
    # Получаем текущее время в Москве
    now = datetime.now(moscow_tz)
    current_hour = now.hour
    current_minute = now.minute

    # Проверяем, попадает ли время в диапазон 10:00 - 22:45
    if not (10 <= current_hour < 22 or (current_hour == 22 and current_minute <= 45)):
        print("Сейчас не время проверки. Ждем следующего окна...")
        return

    # Настраиваем Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без окна браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Проверяю страницу {URL}...")
        driver.get(URL)
        time.sleep(5)  # Ждем загрузки JavaScript

        # Проверяем, есть ли элемент, который указывает на то, что стример в эфире
        try:
            element = driver.find_element(By.CLASS_NAME, "channel-status.online")
            print("Стример в эфире!")
            send_telegram_message("Ами начала подготовку к стриму!")
        except:
            print("Ами пока что не готовится к стриму.")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        driver.quit()

# Запускаем проверку
if __name__ == "__main__":
    while True:
        check_stream()
        time.sleep(1000)  # Проверять каждые 30 минут (1800 секунд)