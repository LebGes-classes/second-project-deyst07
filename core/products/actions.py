"""Продукты - Действия."""

from core.products.model import Product


class ProductActions:
    """Действия с товарами."""

    @staticmethod
    def increase_price(
        product: Product,
        percent: float,
    ):
        """Увеличение цены."""

        product.price += (
            product.price * (percent / 100)
        )

    @staticmethod
    def decrease_price(
        product: Product,
        percent: float,
    ):
        """Уменьшение цены."""

        new_price = (
            product.price
            - product.price * (percent / 100)
        )

        if new_price <= 0:
            raise ValueError(
                'Цена не может быть отрицательной.'
            )

        product.price = new_price

    @staticmethod
    def restock_product(
        product: Product,
        quantity: int,
    ):
        """Пополнение товара."""

        product.add_quantity(quantity)

    @staticmethod
    def sell_product(
        product: Product,
        quantity: int,
    ):
        """Продажа товара."""

        product.remove_quantity(quantity)