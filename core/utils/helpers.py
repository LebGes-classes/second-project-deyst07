"""Утилиты - Помощники."""

from datetime import datetime


class Helpers:
    """Вспомогательные методы."""

    @staticmethod
    def format_money(amount: float) -> str:
        """Форматирование денежных значений."""

        return f'{amount:.2f} ₽'

    @staticmethod
    def current_datetime() -> str:
        """Получение текущей даты."""

        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')