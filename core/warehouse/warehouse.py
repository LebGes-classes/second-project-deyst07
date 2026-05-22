"""Склад - Склад."""

from core.users.employee.model import Employee
from core.utils.generators import IdGenerator
from core.warehouse.warehouse_cell import (
    WarehouseCell,
)


class Warehouse:
    """Класс склада."""

    def __init__(
        self,
        name: str,
        address: str,
        manager: Employee,
        warehouse_id: int | None = None,
    ):
        self.warehouse_id = (
            warehouse_id
            or IdGenerator.generate_warehouse_id()
        )

        self.name = name
        self.address = address
        self.manager = manager

        self.cells: list[WarehouseCell] = []

        self.is_opened = True

    def add_cell(
        self,
        cell: WarehouseCell,
    ):
        """Добавление ячейки."""

        self.cells.append(cell)

    def remove_cell(
        self,
        cell_number: str,
    ):
        """Удаление ячейки."""

        for cell in self.cells:

            if cell.cell_number == cell_number:

                self.cells.remove(cell)

                return

        raise ValueError(
            'Ячейка не найдена.'
        )

    def find_cell(
        self,
        cell_number: str,
    ) -> WarehouseCell:
        """Поиск ячейки."""

        for cell in self.cells:

            if cell.cell_number == cell_number:

                return cell

        raise ValueError(
            'Ячейка не найдена.'
        )

    def change_manager(
        self,
        employee: Employee,
    ):
        """Смена менеджера."""

        self.manager = employee

    def close(self):
        """Закрытие склада."""

        self.is_opened = False

    def open(self):
        """Открытие склада."""

        self.is_opened = True

    @property
    def total_products(self) -> int:
        """Получение количества товаров."""

        total = 0

        for cell in self.cells:

            total += cell.total_products

        return total

    def get_info(self) -> str:
        """Получение информации о складе."""

        return (
            f'ID: {self.warehouse_id}\n'
            f'Название: {self.name}\n'
            f'Адрес: {self.address}\n'
            f'Менеджер: '
            f'{self.manager.full_name}\n'
            f'Ячеек: {len(self.cells)}\n'
            f'Товаров: {self.total_products}\n'
            f'Открыт: {self.is_opened}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'warehouse_id': self.warehouse_id,
            'name': self.name,
            'address': self.address,
            'manager_id': self.manager.user_id,
            'cells': [
                cell.to_dict()
                for cell in self.cells
            ],
            'is_opened': self.is_opened,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        manager: Employee,
    ):
        """Создание объекта из словаря."""

        warehouse = cls(
            name=data['name'],
            address=data['address'],
            manager=manager,
            warehouse_id=data['warehouse_id'],
        )

        warehouse.cells = [
            WarehouseCell.from_dict(cell)
            for cell in data['cells']
        ]

        warehouse.is_opened = (
            data['is_opened']
        )

        return warehouse