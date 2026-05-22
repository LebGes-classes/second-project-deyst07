"""Базовый пользователь - Модель."""

from datetime import date

from core.users.base_user.address import Address
from core.users.base_user.enums import Gender
from core.utils.validators import Validators


class BaseUser:
    """Базовый класс пользователя."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        gender: Gender,
        phone: str,
        email: str,
        address: Address,
        user_id: int,
    ):
        if not Validators.validate_phone(phone):
            raise ValueError('Некорректный номер телефона.')

        if not Validators.validate_email(email):
            raise ValueError('Некорректный email.')

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address

    @property
    def full_name(self) -> str:
        """Получение полного имени."""

        return f'{self.first_name} {self.last_name}'

    def get_info(self) -> str:
        """Получение информации о пользователе."""

        return (
            f'ID: {self.user_id}\n'
            f'Имя: {self.full_name}\n'
            f'Телефон: {self.phone}\n'
            f'Email: {self.email}\n'
            f'Адрес: {self.address.get_full_address()}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat(),
            'gender': self.gender.value,
            'phone': self.phone,
            'email': self.email,
            'address': self.address.to_dict(),
        }