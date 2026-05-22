"""UI - Меню сотрудников."""

from datetime import date

from core.database.database_manager import (
    DatabaseManager,
)
from core.users.base_user.address import (
    Address,
)
from core.users.base_user.enums import (
    EmployeeRole,
    Gender,
)
from core.users.employee.actions import (
    EmployeeActions,
)
from core.users.employee.model import (
    Employee,
)
from core.utils.console import (
    ConsoleManager,
)


def show_employees():
    """Показ сотрудников."""

    ConsoleManager.header(
        'СОТРУДНИКИ'
    )

    users = DatabaseManager.load_users()

    employees = [
        user
        for user in users
        if isinstance(user, Employee)
    ]

    if not employees:

        print('Сотрудников нет.')

        ConsoleManager.pause()

        return

    for employee in employees:

        print(employee.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def create_employee():
    """Создание сотрудника."""

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ СОТРУДНИКА'
        )

        first_name = input('Имя: ')

        last_name = input('Фамилия: ')

        birth_date = date.fromisoformat(
            input(
                'Дата рождения '
                '(YYYY-MM-DD): '
            )
        )

        print('\nПол:')

        print('1. Мужской')

        print('2. Женский')

        gender_choice = input(
            '\nВыберите пол: '
        )

        genders = {
            '1': Gender.MALE,
            '2': Gender.FEMALE,
        }

        gender = genders.get(
            gender_choice
        )

        if not gender:

            raise ValueError(
                'Неверный пол.'
            )

        phone = input('Телефон: ')

        email = input('Email: ')

        country = input('Страна: ')

        city = input('Город: ')

        street = input('Улица: ')

        house_number = input('Дом: ')

        postal_code = input(
            'Почтовый индекс: '
        )

        address = Address(
            country=country,
            city=city,
            street=street,
            house_number=house_number,
            postal_code=postal_code,
        )

        print('\nРоль:')

        print('1. Менеджер')

        print('2. Продавец')

        print('3. Складской работник')

        print('4. Администратор')

        role_choice = input(
            '\nВыберите роль: '
        )

        roles = {
            '1': EmployeeRole.MANAGER,
            '2': EmployeeRole.SELLER,
            '3': (
                EmployeeRole
                .WAREHOUSE_WORKER
            ),
            '4': EmployeeRole.ADMIN,
        }

        role = roles.get(role_choice)

        if not role:

            raise ValueError(
                'Неверная роль.'
            )

        salary = float(
            input('Зарплата: ')
        )

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
            role=role,
            salary=salary,
        )

        DatabaseManager.add_user(
            employee
        )

        print(
            '\nСотрудник успешно создан.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def fire_employee():
    """Увольнение сотрудника."""

    try:

        ConsoleManager.header(
            'УВОЛЬНЕНИЕ СОТРУДНИКА'
        )

        users = DatabaseManager.load_users()

        employees = [
            user
            for user in users
            if isinstance(user, Employee)
        ]

        if not employees:

            print('Сотрудников нет.')

            ConsoleManager.pause()

            return

        for employee in employees:

            print(employee.get_info())

            print('-' * 50)

        employee_id = int(
            input(
                '\nВведите ID сотрудника: '
            )
        )

        employee = next(
            (
                employee
                for employee in employees
                if (
                    employee.user_id
                    == employee_id
                )
            ),
            None,
        )

        if not employee:

            raise ValueError(
                'Сотрудник не найден.'
            )

        EmployeeActions.fire_employee(
            employee
        )

        DatabaseManager.update_user(
            employee
        )

        print(
            '\nСотрудник уволен.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def employee_menu(app_state):
    """Меню сотрудников."""

    while True:

        ConsoleManager.header(
            'СОТРУДНИКИ'
        )

        print(
            '1. Показать сотрудников'
        )

        print(
            '2. Создать сотрудника'
        )

        print(
            '3. Уволить сотрудника'
        )

        print('4. Назад')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                show_employees()

            case '2':

                create_employee()

            case '3':

                fire_employee()

            case '4':

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()