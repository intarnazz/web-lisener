# storage.py
"""
Модуль для работы с локальным хранилищем данных (JSON).
"""

import json
from init import DATA_JSON_FILE


def load_json() -> list:
    """
    Загружает данные из JSON файла.

    :return: список объектов из файла
    """
    try:
        with open(DATA_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {DATA_JSON_FILE} не найден. Возвращаю пустой список.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON ({DATA_JSON_FILE}): {e}")
        return []
