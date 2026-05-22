"""Утилиты - Валидаторы."""

import re


class Validators:
    """Класс валидаторов."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверка email."""

        pattern = (
            r'^[a-zA-Z0-9_.+-]+'
            r'@[a-zA-Z0-9-]+'
            r'\.[a-zA-Z0-9-.]+$'
        )

        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверка номера телефона."""

        pattern = r'^\+?[0-9]{10,15}$'

        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверка цены."""

        return price > 0

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        """Проверка количества."""

        return quantity >= 0