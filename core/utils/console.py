"""Утилиты - Консоль."""

import os


class ConsoleManager:
    """Менеджер консоли."""

    @staticmethod
    def clear():
        """Очистка консоли."""

        os.system(
            'cls'
            if os.name == 'nt'
            else 'clear'
        )

    @staticmethod
    def pause():
        """Пауза консоли."""

        input(
            '\nНажмите Enter '
            'для продолжения...'
        )

    @staticmethod
    def header(title: str):
        """Вывод заголовка."""

        ConsoleManager.clear()

        print(f'=== {title} ===\n')