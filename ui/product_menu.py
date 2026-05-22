"""UI - Меню продуктов."""

from core.database.database_manager import (
    DatabaseManager,
)
from core.products.actions import ProductActions
from core.products.enums import ProductCategory
from core.products.model import Product
from core.utils.console import (
    ConsoleManager,
)


def show_products():
    """Показ товаров."""

    ConsoleManager.header(
        'ТОВАРЫ'
    )

    products = (
        DatabaseManager.load_products()
    )

    if not products:

        print('Товаров нет.')

        ConsoleManager.pause()

        return

    for product in products:

        print(product.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def create_product():
    """Создание товара."""

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ ТОВАРА'
        )

        name = input('Название товара: ')

        print('\nКатегория:')

        print('1. Электроника')
        print('2. Одежда')
        print('3. Продукты')
        print('4. Мебель')
        print('5. Другое')

        category_choice = input(
            '\nВыберите категорию: '
        )

        categories = {
            '1': ProductCategory.ELECTRONICS,
            '2': ProductCategory.CLOTHES,
            '3': ProductCategory.FOOD,
            '4': ProductCategory.FURNITURE,
            '5': ProductCategory.OTHER,
        }

        category = categories.get(
            category_choice
        )

        if not category:

            raise ValueError(
                'Неверная категория.'
            )

        price = float(
            input('Цена: ')
        )

        quantity = int(
            input('Количество: ')
        )

        product = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
        )

        DatabaseManager.add_product(
            product
        )

        print(
            '\nТовар успешно создан.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def update_product():
    """Обновление товара."""

    try:

        ConsoleManager.header(
            'ОБНОВЛЕНИЕ ТОВАРА'
        )

        products = (
            DatabaseManager.load_products()
        )

        if not products:

            print('Товаров нет.')

            ConsoleManager.pause()

            return

        print('ТОВАРЫ:\n')

        for product in products:

            print(product.get_info())

            print('-' * 50)

        product_id = int(
            input(
                '\nВведите ID товара: '
            )
        )

        product = next(
            (
                prod
                for prod in products
                if (
                    prod.product_id
                    == product_id
                )
            ),
            None,
        )

        if not product:

            raise ValueError(
                'Товар не найден.'
            )

        print('\n1. Изменить цену')
        print('2. Пополнить количество')
        print('3. Уменьшить количество')

        action = input(
            '\nВыберите действие: '
        )

        match action:

            case '1':

                new_price = float(
                    input('Новая цена: ')
                )

                product.change_price(
                    new_price
                )

            case '2':

                quantity = int(
                    input('Количество для пополнения: ')
                )

                ProductActions.restock_product(
                    product,
                    quantity,
                )

            case '3':

                quantity = int(
                    input('Количество для продажи: ')
                )

                ProductActions.sell_product(
                    product,
                    quantity,
                )

            case _:

                raise ValueError(
                    'Неверный выбор.'
                )

        DatabaseManager.update_product(
            product
        )

        print(
            '\nТовар успешно обновлен.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def product_menu():
    """Меню товаров."""

    while True:

        ConsoleManager.header(
            'ТОВАРЫ'
        )

        print('1. Показать товары')
        print('2. Создать товар')
        print('3. Обновить товар')
        print('4. Назад')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                show_products()

            case '2':

                create_product()

            case '3':

                update_product()

            case '4':

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()
