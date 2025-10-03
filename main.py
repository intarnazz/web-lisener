# main.py
"""
Главный модуль приложения:
- Запускает основной цикл
- Управляет выбором данных и проверкой ссылок
"""

import time
from selector import select_data
from checker import check_links


def main():
    """
    Основной цикл:
    - пользователь выбирает данные
    - запускается проверка ссылок
    - при отсутствии результатов — пауза или возврат к выбору
    """
    selected_data = select_data()

    while True:
        try:
            found = check_links(selected_data)
            if not found:
                print("\n❌ Ничего не найдено.")
                choice = input(
                    "Нажмите Enter, чтобы вернуться к выбору пути, "
                    "или подождите 60 секунд...\n"
                )
                if choice.strip() == "":
                    selected_data = select_data()
                    continue
            else:
                # если найдено — возвращаемся к выбору
                selected_data = select_data()
                continue
        except Exception as e:
            print(f"Ошибка: {e}")

        time.sleep(60)


if __name__ == "__main__":
    main()
