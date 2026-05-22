"""Утилиты - Генераторы."""

import random
import string


class IdGenerator:
    """Генератор идентификаторов."""

    current_user_id = 1
    current_product_id = 1
    current_order_id = 1
    current_warehouse_id = 1
    current_sales_point_id = 1

    @classmethod
    def reset_all(cls):
        """Сброс всех счетчиков."""
        
        cls.current_user_id = 1
        cls.current_product_id = 1
        cls.current_order_id = 1
        cls.current_warehouse_id = 1
        cls.current_sales_point_id = 1

    @classmethod
    def generate_user_id(cls) -> int:
        """Генерация ID пользователя."""

        user_id = cls.current_user_id
        cls.current_user_id += 1

        return user_id

    @classmethod
    def generate_product_id(cls) -> int:
        """Генерация ID товара."""

        product_id = cls.current_product_id
        cls.current_product_id += 1

        return product_id

    @classmethod
    def generate_order_id(cls) -> int:
        """Генерация ID заказа."""

        order_id = cls.current_order_id
        cls.current_order_id += 1

        return order_id

    @classmethod
    def generate_warehouse_id(cls) -> int:
        """Генерация ID склада."""

        warehouse_id = cls.current_warehouse_id
        cls.current_warehouse_id += 1

        return warehouse_id

    @classmethod
    def generate_sales_point_id(cls) -> int:
        """Генерация ID точки продаж."""

        sales_point_id = cls.current_sales_point_id
        cls.current_sales_point_id += 1

        return sales_point_id


class ArticleGenerator:
    """Генератор артикулов."""

    @staticmethod
    def generate_article(prefix: str = 'PRD') -> str:
        """Генерация артикула."""

        random_part = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6,
            )
        )

        return f'{prefix}-{random_part}'