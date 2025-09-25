# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Читаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    # Если токен не найден, вызываем исключение с понятным сообщением
    raise ValueError("Ошибка: не найден токен бота (BOT_TOKEN) в .env файле.")