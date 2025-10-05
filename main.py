# main.py

import time
import pygame
from selector import Selector
from checker import Checker


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
        self.checker = Checker()

    def main(self):
        """
        Основной цикл:
        - пользователь выбирает данные
        - запускается проверка ссылок
        - при отсутствии результатов — пауза или возврат к выбору
        """

        while True:
            try:
                found = self.checker.check(self.selector.select())
                if not found:
                    print("\n❌ Ничего не найдено.")
                    input(
                        "Нажмите Enter, чтобы вернуться к выбору пути, "
                        "или подождите 60 секунд...\n"
                    )
                    continue
                else:
                    # если найдено — возвращаемся к выбору
                    continue
            except Exception as e:
                print(f"Ошибка: {e}")

            time.sleep(10)


if __name__ == "__main__":
    app = App()
    app.main()
