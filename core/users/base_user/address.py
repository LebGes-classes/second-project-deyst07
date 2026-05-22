"""Базовый пользователь - Адрес."""

class Address:
    """Класс адреса."""

    def __init__(
        self,
        country: str,
        city: str,
        street: str,
        house_number: str,
        postal_code: str,
    ):
        self.country = country
        self.city = city
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code

    def get_full_address(self) -> str:
        """Получение полного адреса."""

        return (
            f'{self.country}, '
            f'{self.city}, '
            f'{self.street}, '
            f'{self.house_number}, '
            f'{self.postal_code}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        return {
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number,
            'postal_code': self.postal_code,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""

        return cls(
            country=data['country'],
            city=data['city'],
            street=data['street'],
            house_number=data['house_number'],
            postal_code=data['postal_code'],
        )