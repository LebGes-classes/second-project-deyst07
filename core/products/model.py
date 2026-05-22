"""Продукты - Модель."""

from core.products.enums import ProductCategory
from core.utils.generators import (
    ArticleGenerator,
    IdGenerator,
)
from core.utils.helpers import Helpers
from core.utils.validators import Validators


class Product:
    """Класс товара."""

    def __init__(
        self,
        name: str,
        category: ProductCategory,
        price: float,
        quantity: int,
        product_id: int | None = None,
    ):
        if not Validators.validate_price(price):
            raise ValueError(
                'Цена должна быть больше нуля.'
            )

        if not Validators.validate_quantity(
            quantity
        ):
            raise ValueError(
                'Количество не может быть отрицательным.'
            )

        self.product_id = (
            product_id
            or IdGenerator.generate_product_id()
        )

        self.article = (
            ArticleGenerator.generate_article()
        )

        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    @property
    def total_price(self) -> float:
        """Получение полной стоимости."""

        return self.price * self.quantity

    def add_quantity(
        self,
        quantity: int,
    ):
        """Добавление количества."""

        self.quantity += quantity

    def remove_quantity(
        self,
        quantity: int,
    ):
        """Уменьшение количества."""

        if quantity > self.quantity:
            raise ValueError(
                'Недостаточно товара.'
            )

        self.quantity -= quantity

    def change_price(
        self,
        new_price: float,
    ):
        """Изменение цены."""

        if not Validators.validate_price(
            new_price
        ):
            raise ValueError(
                'Некорректная цена.'
            )

        self.price = new_price

    def get_info(self) -> str:
        """Получение информации о товаре."""

        return (
            f'ID: {self.product_id}\n'
            f'Артикул: {self.article}\n'
            f'Название: {self.name}\n'
            f'Категория: {self.category.value}\n'
            f'Цена: '
            f'{Helpers.format_money(self.price)}\n'
            f'Количество: {self.quantity}\n'
            f'Общая стоимость: '
            f'{Helpers.format_money(self.total_price)}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'product_id': self.product_id,
            'article': self.article,
            'name': self.name,
            'category': self.category.value,
            'price': self.price,
            'quantity': self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""

        product = cls(
            name=data['name'],
            category=ProductCategory(
                data['category']
            ),
            price=data['price'],
            quantity=data['quantity'],
            product_id=data['product_id'],
        )

        product.article = data['article']

        return product