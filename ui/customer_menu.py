"""UI - Меню покупателей."""

from datetime import date

from core.database.database_manager import (
    DatabaseManager,
)
from core.users.base_user.address import (
    Address,
)
from core.users.base_user.enums import (
    Gender,
)
from core.users.customer.model import (
    Customer,
)
from core.utils.console import (
    ConsoleManager,
)


def show_customers():
    """Показ покупателей."""

    ConsoleManager.header(
        'ПОКУПАТЕЛИ'
    )

    users = DatabaseManager.load_users()

    customers = [
        user
        for user in users
        if isinstance(user, Customer)
    ]

    if not customers:

        print('Покупателей нет.')

        ConsoleManager.pause()

        return

    for customer in customers:

        print(customer.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def create_customer():
    """Создание покупателя."""

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ ПОКУПАТЕЛЯ'
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

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            address=address,
        )

        DatabaseManager.add_user(
            customer
        )

        print(
            '\nПокупатель успешно создан.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def customer_menu(app_state):
    """Меню покупателей."""

    while True:

        ConsoleManager.header(
            'ПОКУПАТЕЛИ'
        )

        print('1. Показать покупателей')
        print('2. Создать покупателя')
        print('3. Назад')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                show_customers()

            case '2':

                create_customer()

            case '3':

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()
