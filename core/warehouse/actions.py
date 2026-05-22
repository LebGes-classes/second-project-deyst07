"""Склад - Действия."""

from core.products.model import Product
from core.sales.sales_point import SalesPoint
from core.warehouse.warehouse import Warehouse


class WarehouseActions:
    """Действия со складом."""

    @staticmethod
    def add_product_to_cell(
        warehouse: Warehouse,
        cell_number: str,
        product: Product,
    ):
        """Добавление товара в ячейку."""

        cell = warehouse.find_cell(
            cell_number
        )

        cell.add_product(product)

    @staticmethod
    def remove_product_from_cell(
        warehouse: Warehouse,
        cell_number: str,
        product_id: int,
        quantity: int,
    ):
        """Удаление товара."""

        cell = warehouse.find_cell(
            cell_number
        )

        cell.remove_product(
            product_id,
            quantity,
        )

    @staticmethod
    def move_product_between_cells(
        warehouse: Warehouse,
        from_cell_number: str,
        to_cell_number: str,
        product_id: int,
        quantity: int,
    ):
        """Перемещение товара между ячейками."""

        from_cell = warehouse.find_cell(
            from_cell_number
        )

        to_cell = warehouse.find_cell(
            to_cell_number
        )

        product = from_cell.find_product(
            product_id
        )

        moved_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            quantity=quantity,
            product_id=product.product_id,
        )

        from_cell.remove_product(
            product_id,
            quantity,
        )

        to_cell.add_product(
            moved_product
        )

    @staticmethod
    def move_product_to_sales_point(
        warehouse: Warehouse,
        sales_point: SalesPoint,
        cell_number: str,
        product_id: int,
        quantity: int,
    ):
        """Перемещение товара в точку продаж."""

        cell = warehouse.find_cell(
            cell_number
        )

        product = cell.find_product(
            product_id
        )

        moved_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            quantity=quantity,
            product_id=product.product_id,
        )

        cell.remove_product(
            product_id,
            quantity,
        )

        sales_point.add_product(
            moved_product
        )