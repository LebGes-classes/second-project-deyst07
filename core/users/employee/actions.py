"""Сотрудники - Действия."""

from core.users.employee.model import Employee


class EmployeeActions:
    """Действия с сотрудниками."""

    @staticmethod
    def hire_employee(employee: Employee):
        """Найм сотрудника."""

        employee.hire()

    @staticmethod
    def fire_employee(employee: Employee):
        """Увольнение сотрудника."""

        employee.fire()

    @staticmethod
    def change_salary(
        employee: Employee,
        new_salary: float,
    ):
        """Изменение зарплаты."""

        if new_salary <= 0:
            raise ValueError(
                'Зарплата должна быть больше нуля.'
            )

        employee.salary = new_salary