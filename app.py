import requests
import json
import time
import pygame
import webbrowser
from bs4 import BeautifulSoup


BASE_URL = "https://fogplay.mts.ru/computer/"
AUDIO_FILE = "./Kuvaev_1[Master]+вокал13дб.обр.mp3"

# Инициализация звука
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


def check_links(data):
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
                        webbrowser.open(play_url)
                        input("⏸ Нажмите Enter, чтобы остановить звук и продолжить...")
                        pygame.mixer.music.stop()
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")


def main():
    while True:
        try:
            data = load_json()
            check_links(data)
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(60)


if __name__ == "__main__":
    main()