"""Сотрудники - Модель."""

from datetime import date

from core.users.base_user.address import Address
from core.users.base_user.enums import (
    EmployeeRole,
    Gender,
)
from core.users.base_user.model import BaseUser
from core.utils.generators import IdGenerator


class Employee(BaseUser):
    """Класс сотрудника."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        gender: Gender,
        phone: str,
        email: str,
        address: Address,
        role: EmployeeRole,
        salary: float,
        user_id: int | None = None,
    ):
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            user_id=(
                user_id
                or IdGenerator.generate_user_id()
            ),
        )

        self.role = role
        self.salary = salary
        self.is_working = True

    def fire(self):
        """Увольнение сотрудника."""

        self.is_working = False

    def hire(self):
        """Повторный найм сотрудника."""

        self.is_working = True

    def get_info(self) -> str:
        """Получение информации о сотруднике."""

        return (
            f'{super().get_info()}\n'
            f'Роль: {self.role.value}\n'
            f'Зарплата: {self.salary}\n'
            f'Работает: {self.is_working}'
        )

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь."""

        data = super().to_dict()

        data.update({
            'user_type': 'employee',
            'role': self.role.value,
            'salary': self.salary,
            'is_working': self.is_working,
        })

        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Создание объекта из словаря."""

        employee =  cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=date.fromisoformat(
                data['birth_date']
            ),
            gender=Gender(data['gender']),
            phone=data['phone'],
            email=data['email'],
            address=Address.from_dict(
                data['address']
            ),
            role=EmployeeRole(data['role']),
            salary=data['salary'],
            user_id=data['user_id'],
        )
        employee.is_working = (
        data['is_working']
    )

        return employee
            