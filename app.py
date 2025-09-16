from InquirerPy import inquirer
import requests
import json
import time
import pygame
import webbrowser
import subprocess
import shutil
import sys
from bs4 import BeautifulSoup


BASE_URL = "https://fogplay.mts.ru/computer/"
AUDIO_FILE = "./Kuvaev_1[Master]+вокал13дб.обр.mp3"

pygame.init()
pygame.mixer.init()


def load_json():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def play_audio():
    try:
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")


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


def save_json(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def move_to_top(path):
    data = load_json()
    for i, item in enumerate(data):
        if item.get("path") == path:
            # Удаляем и вставляем в начало
            obj = data.pop(i)
            data.insert(0, obj)
            save_json(data)
            print(f"📌 Объект '{path}' перемещён в начало списка.")
            break


def open_in_private(url):
    """Открывает ссылку в приватном/инкогнито режиме, если доступен браузер."""
    browsers = [
        ("chrome", ["--incognito"]),
        ("google-chrome", ["--incognito"]),
        ("chromium", ["--incognito"]),
        ("edge", ["--inprivate"]),
        ("msedge", ["--inprivate"]),
        ("firefox", ["--private-window"]),
    ]

    for browser, args in browsers:
        path = shutil.which(browser)
        if path:
            try:
                subprocess.Popen([path] + args + [url])
                print(f"🌐 Открыто в приватном режиме ({browser})")
                return
            except Exception as e:
                print(f"Ошибка запуска {browser}: {e}")

    # fallback — обычный webbrowser
    import webbrowser

    print("⚠ Не найден подходящий браузер, открываю обычным способом.")
    webbrowser.open(url)


def check_links(data):
    found_any = False
    for item in data:
        path = item.get("path")
        codes = item.get("code")

        if isinstance(codes, str):
            codes = [codes]
        if not path or not codes:
            continue

        url = BASE_URL + path.strip("/") + "/"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text

            for code in codes:
                if code in html:
                    play_url = extract_play_link(html, code)
                    if play_url:
                        print(f"\n🔔 НАЙДЕНО: {code} на {url}")
                        print(f"▶ Открытие ссылки: {play_url}")
                        play_audio()
                        open_in_private(play_url)
                        input("⏸ Нажмите Enter, чтобы остановить звук и продолжить...")
                        pygame.mixer.music.stop()
                        move_to_top(path)  # 📌 Перемещаем в начало
                        found_any = True
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")

    return found_any


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
        return [item for item in data if item["path"] == selected]


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
        except Exception as e:
            print(f"Ошибка: {e}")

        time.sleep(60)


if __name__ == "__main__":
    main()
