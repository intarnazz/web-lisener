# init.py
"""
Модуль инициализации приложения:
- Импорт внешних библиотек
- Загрузка .env переменных
- Инициализация pygame
- Определение констант и заголовков HEADERS
"""

import os
import json
import time
import pygame
import webbrowser
import requests
from InquirerPy import inquirer
from bs4 import BeautifulSoup
from dotenv import load_dotenv


# Загружаем переменные окружения из .env
load_dotenv()

# Константы
BASE_URL = "https://fogplay.mts.ru/computer/"
AUDIO_FILE = "./src/sound/bonfire.mp3"
DATA_JSON_FILE = "./src/storage/data.json"

# Заголовки из .env
HEADERS = json.loads(os.getenv("HEADERS"))

# Инициализация Pygame
pygame.init()
pygame.mixer.init()
