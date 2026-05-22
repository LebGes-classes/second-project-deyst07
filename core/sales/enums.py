"""Продажи - Перечисления."""

from enum import Enum


class OrderStatus(Enum):
    """Статусы заказа."""

    CREATED = 'created'
    PAID = 'paid'
    RETURNED = 'returned'
    CANCELLED = 'cancelled'