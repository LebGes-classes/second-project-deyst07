"""Покупатели - Действия."""

from core.users.customer.model import Customer


class CustomerActions:
    """Действия с покупателями."""

    @staticmethod
    def spend_bonus_points(
        customer: Customer,
        points: int,
    ):
        """Списание бонусов."""

        if points > customer.bonus_points:
            raise ValueError(
                'Недостаточно бонусов.'
            )

        customer.bonus_points -= points

    @staticmethod
    def reset_bonus_points(
        customer: Customer,
    ):
        """Сброс бонусов."""

        customer.bonus_points = 0