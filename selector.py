# selector.py
"""
Модуль выбора данных:
- Интерактивный выбор пути поиска (InquirerPy)
- Обновление порядка элементов в JSON
"""

import json
from InquirerPy import inquirer
from init import DATA_JSON_FILE
from storage import load_json


def select_data() -> list:
    """
    Дает пользователю выбрать путь для поиска.
    Если выбран "Проверять все" — возвращает весь список.
    Если выбран конкретный путь — перемещает его в начало и обновляет JSON.

    :return: список выбранных элементов (всегда список, даже если один элемент)
    """
    data = load_json()
    choices = [item["path"] for item in data]
    choices.insert(0, "🔎 Проверять все")

    selected = inquirer.select(
        message="Выберите путь для поиска:",
        choices=choices,
        default="🔎 Проверять все",
    ).execute()

    if selected == "🔎 Проверять все":
        return data
    else:
        # перемещаем выбранный объект в начало
        selected_item = next((item for item in data if item["path"] == selected), None)
        if selected_item:
            data.remove(selected_item)
            data.insert(0, selected_item)

            # сохраняем обновлённый порядок
            with open(DATA_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        return [selected_item] if selected_item else []
