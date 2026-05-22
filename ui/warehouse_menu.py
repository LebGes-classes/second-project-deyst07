"""UI - Меню склада."""

from core.database.database_manager import (
    DatabaseManager,
)
from core.products.actions import ProductActions
from core.products.enums import ProductCategory
from core.products.model import Product
from core.users.employee.model import Employee
from core.warehouse.warehouse import Warehouse
from core.warehouse.warehouse_cell import WarehouseCell
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


def select_warehouse(app_state):
    """Выбор склада пользователем.

    Args:
        app_state: Состояние приложения.

    Returns:
        Выбранный склад или None.
    """

    if not app_state.warehouses:

        print('Складов нет.')

        ConsoleManager.pause()

        return None

    print('СКЛАДЫ:\n')

    for warehouse in app_state.warehouses:

        print(
            f'{warehouse.warehouse_id}. '
            f'{warehouse.name} - '
            f'{warehouse.address}'
        )

        print('-' * 50)

    try:

        warehouse_id = int(
            input(
                '\nВведите ID склада: '
            )
        )

        warehouse = next(
            (
                wh
                for wh in app_state.warehouses
                if wh.warehouse_id == warehouse_id
            ),
            None,
        )

        if not warehouse:

            raise ValueError(
                'Склад не найден.'
            )

        return warehouse

    except ValueError as error:

        print(f'\nОшибка: {error}')

        ConsoleManager.pause()

        return None


def show_warehouses(app_state):
    """Показ складов.

    Args:
        app_state: Состояние приложения.
    """

    ConsoleManager.header(
        'СКЛАДЫ'
    )

    if not app_state.warehouses:

        print('Складов нет.')

        ConsoleManager.pause()

        return

    for warehouse in app_state.warehouses:

        print(warehouse.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def create_warehouse(app_state):
    """Создание склада.

    Args:
        app_state: Состояние приложения.
    """

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ СКЛАДА'
        )

        users = DatabaseManager.load_users()

        employees = [
            user
            for user in users
            if isinstance(user, Employee)
        ]

        if not employees:

            print(
                'Сначала создайте сотрудников.'
            )

            ConsoleManager.pause()

            return

        print('СОТРУДНИКИ:\n')

        for employee in employees:

            print(employee.get_info())

            print('-' * 50)

        manager_id = int(
            input(
                '\nВведите ID менеджера: '
            )
        )

        manager = next(
            (
                employee
                for employee in employees
                if (
                    employee.user_id
                    == manager_id
                )
            ),
            None,
        )

        if not manager:

            raise ValueError(
                'Менеджер не найден.'
            )

        name = input(
            'Название склада: '
        )

        address = input(
            'Адрес склада: '
        )

        warehouse = Warehouse(
            name=name,
            address=address,
            manager=manager,
        )

        app_state.warehouses.append(
            warehouse
        )

        DatabaseManager.add_warehouse(
            warehouse
        )

        print(
            '\nСклад успешно создан.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def create_cell(app_state):
    """Создание ячейки.

    Args:
        app_state: Состояние приложения.
    """

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ ЯЧЕЙКИ'
        )

        warehouse = select_warehouse(app_state)

        if not warehouse:

            return

        cell_number = input(
            'Номер ячейки: '
        )

        cell = WarehouseCell(
            cell_number=cell_number,
        )

        warehouse.add_cell(cell)

        DatabaseManager.update_warehouse(
            warehouse
        )

        print(
            '\nЯчейка успешно создана.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def show_cells(app_state):
    """Показ ячеек выбранного склада.

    Args:
        app_state: Состояние приложения.
    """

    ConsoleManager.header(
        'ЯЧЕЙКИ'
    )

    warehouse = select_warehouse(app_state)

    if not warehouse:

        return

    print(f'\nСклад: {warehouse.name}\n')

    if not warehouse.cells:

        print('Ячеек нет.')

        ConsoleManager.pause()

        return

    for cell in warehouse.cells:

        print(cell.get_info())

        if cell.products:
            print('  Товары в ячейке:')
            for product in cell.products:
                print(f'    - ID: {product.product_id}, Название: {product.name}, Количество: {product.quantity} шт.')

        print('-' * 30)

    ConsoleManager.pause()


def add_product_to_cell(app_state):
    """Добавление товара в ячейку.

    Args:
        app_state: Состояние приложения.
    """

    try:

        ConsoleManager.header(
            'ДОБАВЛЕНИЕ ТОВАРА В ЯЧЕЙКУ'
        )

        warehouse = select_warehouse(app_state)

        if not warehouse:

            return

        products = (
            DatabaseManager.load_products()
        )

        if not products:

            print('Товаров нет.')

            ConsoleManager.pause()

            return

        if not warehouse.cells:

            print(
                '\nНа складе нет ячеек.'
            )

            ConsoleManager.pause()

            return

        print('\nЯЧЕЙКИ:\n')

        for cell in warehouse.cells:

            print(cell.get_info())

            if cell.products:
                print('  Товары в ячейке:')
                for product in cell.products:
                    print(f'    - ID: {product.product_id}, Название: {product.name}, Количество: {product.quantity} шт.')

            print('-' * 30)

        cell_number = input(
            '\nВведите номер ячейки: '
        )

        print('\nТОВАРЫ:\n')

        for product in products:

            print(product.get_info())

            print('-' * 50)

        product_id = int(
            input(
                '\nВведите ID товара: '
            )
        )

        quantity = int(
            input('Количество: ')
        )

        product = next(
            (
                product
                for product in products
                if (
                    product.product_id
                    == product_id
                )
            ),
            None,
        )

        if not product:

            raise ValueError(
                'Товар не найден.'
            )

        moved_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            quantity=quantity,
            product_id=product.product_id,
        )

        from core.warehouse.actions import (
            WarehouseActions,
        )

        (
            WarehouseActions
            .add_product_to_cell(
                warehouse=warehouse,
                cell_number=cell_number,
                product=moved_product,
            )
        )

        DatabaseManager.update_warehouse(
            warehouse
        )

        print(
            '\nТовар успешно добавлен в ячейку.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def move_product_between_cells(app_state):
    """Перемещение товара между ячейками.

    Args:
        app_state: Состояние приложения.
    """

    try:

        ConsoleManager.header(
            'ПЕРЕМЕЩЕНИЕ ТОВАРА'
        )

        warehouse = select_warehouse(app_state)

        if not warehouse:

            return

        if len(warehouse.cells) < 2:

            print(
                '\nНужно минимум 2 ячейки.'
            )

            ConsoleManager.pause()

            return

        print('\nЯЧЕЙКИ:\n')

        for cell in warehouse.cells:

            print(cell.get_info())

            if cell.products:
                print('  Товары в ячейке:')
                for product in cell.products:
                    print(f'    - ID: {product.product_id}, Название: {product.name}, Количество: {product.quantity} шт.')

            print('-' * 30)

        from_cell = input(
            '\nИз ячейки: '
        )

        to_cell = input(
            'В ячейку: '
        )

        product_id = int(
            input('ID товара: ')
        )

        quantity = int(
            input('Количество: ')
        )

        from core.warehouse.actions import (
            WarehouseActions,
        )

        (
            WarehouseActions
            .move_product_between_cells(
                warehouse=warehouse,
                from_cell_number=from_cell,
                to_cell_number=to_cell,
                product_id=product_id,
                quantity=quantity,
            )
        )

        DatabaseManager.update_warehouse(
            warehouse
        )

        print(
            '\nТовар успешно перемещен.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def warehouse_menu(app_state):
    """Меню склада.

    Args:
        app_state: Состояние приложения.
    """

    while True:

        ConsoleManager.header(
            'СКЛАД'
        )

        print('1. Показать склады')
        print('2. Создать склад')
        print('3. Создать ячейку')
        print('4. Показать ячейки')
        print('5. Добавить товар в ячейку')
        print('6. Переместить товар между ячейками')
        print('7. Назад')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                show_warehouses(app_state)

            case '2':

                create_warehouse(app_state)

            case '3':

                create_cell(app_state)

            case '4':

                show_cells(app_state)

            case '5':

                add_product_to_cell(
                    app_state
                )

            case '6':

                move_product_between_cells(
                    app_state
                )

            case '7':

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()
