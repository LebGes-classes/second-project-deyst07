"""Продажи - Точка продаж."""

from core.products.model import Product
from core.users.employee.model import Employee
from core.utils.generators import (
    IdGenerator,
)
from core.utils.helpers import Helpers


class SalesPoint:
    """Класс точки продаж."""

    def __init__(
        self,
        name: str,
        address: str,
        sales_point_id: int | None = None,
        warehouse_id: int | None = None,
    ):
        self.sales_point_id = (
            sales_point_id
            or IdGenerator.generate_sales_point_id()
        )

        self.name = name
        self.address = address
        self.warehouse_id = warehouse_id

        self.employees: list[Employee] = []
        self.products: list[Product] = []

        self.total_income = 0.0

        self.is_opened = True

    def add_employee(
        self,
        employee: Employee,
    ):
        """Добавление сотрудника."""

        self.employees.append(employee)

    def remove_employee(
        self,
        employee_id: int,
    ):
        """Удаление сотрудника."""

        for employee in self.employees:

            if employee.user_id == employee_id:

                self.employees.remove(employee)

                return

        raise ValueError(
            'Сотрудник не найден.'
        )

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

    def close(self):
        """Закрытие точки продаж."""

        self.is_opened = False

    def open(self):
        """Открытие точки продаж."""

        self.is_opened = True

    def get_info(self) -> str:
        """Получение информации о точке продаж."""

        return (
            f'ID: {self.sales_point_id}\n'
            f'Название: {self.name}\n'
            f'Адрес: {self.address}\n'
            f'Сотрудников: '
            f'{len(self.employees)}\n'
            f'Товаров: '
            f'{len(self.products)}\n'
            f'Доход: '
            f'{Helpers.format_money(self.total_income)}\n'
            f'Открыт: {self.is_opened}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'sales_point_id': self.sales_point_id,
            'name': self.name,
            'address': self.address,
            'warehouse_id': self.warehouse_id,
            'employees': [
                employee.user_id
                for employee in self.employees
            ],
            'products': [
                product.to_dict()
                for product in self.products
            ],
            'total_income': self.total_income,
            'is_opened': self.is_opened,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        employees: list[Employee],
    ):
        """Создание объекта из словаря."""

        sales_point = cls(
            name=data['name'],
            address=data['address'],
            sales_point_id=data[
                'sales_point_id'
            ],
            warehouse_id=data.get('warehouse_id'),
        )

        sales_point.employees = employees

        sales_point.products = [
            Product.from_dict(product)
            for product in data['products']
        ]

        sales_point.total_income = (
            data['total_income']
        )

        sales_point.is_opened = (
            data['is_opened']
        )

        return sales_point