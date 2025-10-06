# main.py

import pygame
from selector import Selector


class App:
    """
    Главный модуль приложения:
    - Запускает основной цикл
    - Управляет выбором данных и проверкой ссылок
    """

    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()

        self.selector = Selector()

    def main(self):
        """
        Основной цикл:
        - пользователь выбирает данные
        - запускается проверка ссылок
        - при отсутствии результатов — пауза или возврат к выбору
        """

        while True:
            self.selector.run()


if __name__ == "__main__":
    app = App()
    app.main()
