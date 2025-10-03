import requests
import json
import time
import pygame
import webbrowser
import os
from InquirerPy import inquirer
from bs4 import BeautifulSoup
from dotenv import load_dotenv


BASE_URL = "https://fogplay.mts.ru/computer/"
AUDIO_FILE = "./src/sound/item.mp3"
DATA_JSON_FILE = "./src/storage/data.json"

load_dotenv()
HEADERS = json.loads(os.getenv("HEADERS"))

pygame.init()
pygame.mixer.init()


def load_json():
    with open(DATA_JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def play_audio():
    try:
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play(1)  # воспроизведение один раз
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")


def stop_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def extract_play_link(html, target_code):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="card")

    for card in cards:
        title = card.find("p", class_="card__title")
        if title and target_code in title.text:
            play_button = card.find("a", class_="button js-play")
            if play_button and "href" in play_button.attrs:
                return "https://fogplay.mts.ru" + play_button["href"]
    return None


def check_links(data):
    for item in data:
        path = item.get("path")
        codes = item.get("code")

        if isinstance(codes, str):
            codes = [codes]
        if not path or not codes:
            continue

        for page in range(1, 3):  # проверяем страницы 1 и 2
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

                            # звук один раз
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


def select_data():
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

            # сохраняем обновлённый порядок в JSON
            with open(DATA_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        return [selected_item] if selected_item else []


def main():
    selected_data = select_data()

    while True:
        try:
            found = check_links(selected_data)
            if not found:
                print("\n❌ Ничего не найдено.")
                choice = input(
                    "Нажмите Enter, чтобы вернуться к выбору пути, или подождите 60 секунд...\n"
                )
                if choice.strip() == "":
                    selected_data = select_data()
                    continue
            else:
                # если найдено — возвращаемся к выбору пути
                selected_data = select_data()
                continue
        except Exception as e:
            print(f"Ошибка: {e}")

        time.sleep(60)


if __name__ == "__main__":
    main()
