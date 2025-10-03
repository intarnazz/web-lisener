# checker.py
"""
Модуль проверки ссылок:
- Обходит страницы каталога
- Ищет коды игр
- При нахождении воспроизводит звук и предлагает действие пользователю
"""

import requests
import webbrowser
from InquirerPy import inquirer

from init import BASE_URL, HEADERS
from parser import extract_play_link
from audio import play_audio, stop_audio


def check_links(data: list) -> bool:
    """
    Проверяет наличие указанных кодов на страницах.

    :param data: список объектов вида {"path": ..., "code": ...}
    :return: True, если найдена хотя бы одна ссылка, иначе False
    """
    for item in data:
        path = item.get("path")
        codes = item.get("code")

        if isinstance(codes, str):
            codes = [codes]
        if not path or not codes:
            continue

        # проверяем первые две страницы
        for page in range(1, 3):
            url = f"{BASE_URL}{path}/?slug={path}&page={page}"

            try:
                print(f"🔎 Проверка {url} ...")
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                html = response.text

                for code in codes:
                    if code in html:
                        play_url = extract_play_link(html, code)
                        if play_url:
                            print(f"\n🔔 НАЙДЕНО: {code} на {url}")

                            # звук
                            play_audio()

                            # выбор действия
                            choice = inquirer.select(
                                message="Выберите действие:",
                                choices=["▶ Открыть ссылку", "↩ Стартовое меню"],
                                default="▶ Открыть ссылку",
                            ).execute()

                            stop_audio()

                            if choice == "▶ Открыть ссылку":
                                webbrowser.open(play_url)

                            return True
            except Exception as e:
                print(f"Ошибка при запросе {url}: {e}")

    return False
