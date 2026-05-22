"""Покупатели - Модель."""

from datetime import date

from core.users.base_user.address import Address
from core.users.base_user.enums import Gender
from core.users.base_user.model import BaseUser
from core.utils.generators import IdGenerator


class Customer(BaseUser):
    """Класс покупателя."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        gender: Gender,
        phone: str,
        email: str,
        address: Address,
        user_id: int | None = None,
    ):
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            user_id=(
                user_id
                or IdGenerator.generate_user_id()
            ),
        )

        self.bonus_points = 0
        self.total_purchases = 0.0

    def add_bonus_points(
        self,
        points: int,
    ):
        """Добавление бонусов."""

        self.bonus_points += points

    def add_purchase_amount(
        self,
        amount: float,
    ):
        """Добавление суммы покупок."""

        self.total_purchases += amount

    def get_info(self) -> str:
        """Получение информации о покупателе."""

        return (
            f'{super().get_info()}\n'
            f'Бонусы: {self.bonus_points}\n'
            f'Сумма покупок: '
            f'{self.total_purchases}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        data = super().to_dict()

        data.update({
            'user_type': 'customer',
            'bonus_points': self.bonus_points,
            'total_purchases': self.total_purchases,
        })

        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""

        customer = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=date.fromisoformat(
                data['birth_date']
            ),
            gender=Gender(data['gender']),
            phone=data['phone'],
            email=data['email'],
            address=Address.from_dict(
                data['address']
            ),
            user_id=data['user_id'],
        )

        customer.bonus_points = (
            data['bonus_points']
        )

        customer.total_purchases = (
            data['total_purchases']
        )

        return customer