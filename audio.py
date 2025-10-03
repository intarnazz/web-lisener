# audio.py
"""
Модуль для работы со звуком:
- Воспроизведение аудио
- Остановка аудио
"""

import pygame
from init import AUDIO_FILE


def play_audio():
    """Воспроизводит аудиофайл один раз."""
    try:
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play(1)  # 1 = проиграть один раз
    except Exception as e:
        print(f"Ошибка при воспроизведении звука: {e}")


def stop_audio():
    """Останавливает воспроизведение, если оно идёт."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
