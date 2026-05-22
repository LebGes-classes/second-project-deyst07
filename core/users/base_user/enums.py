"""Базовый пользователь - Перечисления."""

from enum import Enum


class Gender(Enum):
    """Перечисление полов."""

    MALE = 'male'
    FEMALE = 'female'


class EmployeeRole(Enum):
    """Перечисление ролей сотрудников."""

    MANAGER = 'Менеджер'
    SELLER = 'Продавец'
    WAREHOUSE_WORKER = 'Складской работник'
    ADMIN = 'Администратор'