"""Продукты - Перечисления."""

from enum import Enum


class ProductCategory(Enum):
    """Категории товаров."""

    FOOD = 'food'
    ELECTRONICS = 'electronics'
    CLOTHES = 'clothes'
    FURNITURE = 'furniture'
    OTHER = 'other'