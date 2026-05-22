"""Склад - Ячейка склада."""

from core.products.model import Product


class WarehouseCell:
    """Класс ячейки склада."""

    def __init__(
        self,
        cell_number: str,
    ):
        self.cell_number = cell_number
        self.products: list[Product] = []

    def add_product(
        self,
        product: Product,
    ):
        """Добавление товара."""

        for existing_product in self.products:

            if (
                existing_product.product_id
                == product.product_id
            ):
                existing_product.add_quantity(
                    product.quantity
                )

                return

        self.products.append(product)

    def remove_product(
        self,
        product_id: int,
        quantity: int,
    ):
        """Удаление товара."""

        for product in self.products:

            if product.product_id == product_id:

                product.remove_quantity(quantity)

                if product.quantity == 0:

                    self.products.remove(product)

                return

        raise ValueError(
            'Товар не найден.'
        )

    def find_product(
        self,
        product_id: int,
    ) -> Product:
        """Поиск товара."""

        for product in self.products:

            if product.product_id == product_id:

                return product

        raise ValueError(
            'Товар не найден.'
        )

    @property
    def total_products(self) -> int:
        """Получение количества товаров."""

        total = 0

        for product in self.products:

            total += product.quantity

        return total

    def get_info(self) -> str:
        """Получение информации о ячейке."""

        info = (
            f'Ячейка: {self.cell_number}\n'
            f'Товаров видов: {len(self.products)}\n'
            f'Общее количество единиц: '
            f'{self.total_products}\n'
            f'Товары:\n'
        )

        for product in self.products:
            info += (
                f'  - ID: {product.product_id}, '
                f'{product.name}, '
                f'Кол-во: {product.quantity}\n'
            )

        return info

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'cell_number': self.cell_number,
            'products': [
                product.to_dict()
                for product in self.products
            ],
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""

        from core.products.model import Product

        cell = cls(
            cell_number=data['cell_number'],
        )

        cell.products = [
            Product.from_dict(product)
            for product in data['products']
        ]

        return cell