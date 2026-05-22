"""Продажи - Действия."""

from core.products.model import Product
from core.sales.order import Order
from core.sales.sales_point import SalesPoint
from core.users.customer.model import Customer


class SalesActions:
    """Действия с продажами."""

    @staticmethod
    def create_order(
        customer: Customer,
    ) -> Order:
        """Создание заказа."""

        return Order(
            customer=customer,
        )

    @staticmethod
    def add_product_to_order(
        sales_point: SalesPoint,
        order: Order,
        product_id: int,
        quantity: int,
    ):
        """Добавление товара в заказ."""

        sales_product = (
            sales_point.find_product(
                product_id
            )
        )

        if (
            sales_product.quantity
            < quantity
        ):
            raise ValueError(
                'Недостаточно товара.'
            )

        order_product = Product(
            name=sales_product.name,
            category=sales_product.category,
            price=sales_product.price,
            quantity=quantity,
            product_id=(
                sales_product.product_id
            ),
        )

        order.add_product(order_product)

    @staticmethod
    def sell_products(
        sales_point: SalesPoint,
        order: Order,
    ):
        """Продажа товаров."""

        for order_product in order.products:

            sales_product = (
                sales_point.find_product(
                    order_product.product_id
                )
            )

            sales_product.remove_quantity(
                order_product.quantity
            )

        sales_point.total_income += (
            order.total_price
        )

        order.customer.add_purchase_amount(
            order.total_price
        )

        bonus_points = int(
            order.total_price // 10
        )

        order.customer.add_bonus_points(
            bonus_points
        )

        order.pay()

    @staticmethod
    def return_products(
        sales_point: SalesPoint,
        order: Order,
    ):
        """Возврат товаров."""

        for order_product in order.products:

            sales_product = (
                sales_point.find_product(
                    order_product.product_id
                )
            )

            sales_product.add_quantity(
                order_product.quantity
            )

        sales_point.total_income -= (
            order.total_price
        )

        order.return_order()