# audio.py

import pygame
from setings import Setings


class Audio:
    """
    Модуль для работы со звуком:
    - Воспроизведение аудио
    - Остановка аудио
    """

    def __init__(self):
        self.setings = Setings()

    def play(self):
        """Воспроизводит аудиофайл один раз."""
        try:
            pygame.mixer.music.load(self.setings.AUDIO_FILE)
            pygame.mixer.music.play(1)  # 1 = проиграть один раз
        except Exception as e:
            print(f"Ошибка при воспроизведении звука: {e}")

    def stop(self):
        """Останавливает воспроизведение, если оно идёт."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
