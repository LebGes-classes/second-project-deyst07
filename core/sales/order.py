"""Продажи - Заказ."""

from datetime import datetime

from core.products.model import Product
from core.sales.enums import OrderStatus
from core.users.customer.model import Customer
from core.utils.generators import IdGenerator
from core.utils.helpers import Helpers


class Order:
    """Класс заказа."""

    def __init__(
        self,
        customer: Customer,
        order_id: int | None = None,
    ):
        self.order_id = (
            order_id
            or IdGenerator.generate_order_id()
        )

        self.customer = customer

        self.products: list[Product] = []

        self.status = OrderStatus.CREATED

        self.created_at = datetime.now()

    @property
    def total_price(self) -> float:
        """Получение полной стоимости."""

        total_price = 0.0

        for product in self.products:

            total_price += product.total_price

        return total_price

    def add_product(
        self,
        product: Product,
    ):
        """Добавление товара."""

        self.products.append(product)

    def remove_product(
        self,
        product_id: int,
    ):
        """Удаление товара."""

        for product in self.products:

            if product.product_id == product_id:

                self.products.remove(product)

                return

        raise ValueError(
            'Товар не найден.'
        )

    def pay(self):
        """Оплата заказа."""

        self.status = OrderStatus.PAID

    def cancel(self):
        """Отмена заказа."""

        self.status = OrderStatus.CANCELLED

    def return_order(self):
        """Возврат заказа."""

        self.status = OrderStatus.RETURNED

    def get_info(self) -> str:
        """Получение информации о заказе."""

        return (
            f'ID заказа: {self.order_id}\n'
            f'Покупатель: '
            f'{self.customer.full_name}\n'
            f'Товаров: {len(self.products)}\n'
            f'Сумма заказа: '
            f'{Helpers.format_money(self.total_price)}\n'
            f'Статус: {self.status.value}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'order_id': self.order_id,
            'customer_id': self.customer.user_id,
            'products': [
                product.to_dict()
                for product in self.products
            ],
            'status': self.status.value,
            'created_at': (
                self.created_at.isoformat()
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        customer: Customer,
    ):
        """Создание объекта из словаря."""

        order = cls(
            customer=customer,
            order_id=data['order_id'],
        )

        order.products = [
            Product.from_dict(product)
            for product in data['products']
        ]

        order.status = OrderStatus(
            data['status']
        )

        order.created_at = (
            datetime.fromisoformat(
                data['created_at']
            )
        )

        return order