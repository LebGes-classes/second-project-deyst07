"""UI - Меню продаж."""

from core.database.database_manager import (
    DatabaseManager,
)
from core.sales.actions import (
    SalesActions,
)
from core.sales.sales_point import (
    SalesPoint,
)
from core.users.customer.model import (
    Customer,
)
from core.users.employee.model import (
    Employee,
)
from core.utils.console import (
    ConsoleManager,
)


def get_sales_point_by_id(
    app_state,
    sales_point_id: int,
):
    """Получение точки продаж по ID."""

    for sales_point in app_state.sales_points:

        if (
            sales_point.sales_point_id
            == sales_point_id
        ):

            return sales_point

    raise ValueError(
        'Точка продаж не найдена.'
    )


def select_sales_point(app_state):
    """Выбор точки продаж пользователем."""

    if not app_state.sales_points:

        print('Точек продаж нет.')

        ConsoleManager.pause()

        return None

    print('ТОЧКИ ПРОДАЖ:\n')

    for sales_point in app_state.sales_points:

        print(
            f'{sales_point.sales_point_id}. '
            f'{sales_point.name} - '
            f'{sales_point.address}'
        )

        print('-' * 50)

    try:

        sales_point_id = int(
            input(
                '\nВведите ID точки продаж: '
            )
        )

        return get_sales_point_by_id(
            app_state,
            sales_point_id,
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

        ConsoleManager.pause()

        return None


def create_first_sales_point(app_state):
    """Создание первой точки продаж."""

    sales_point = SalesPoint(
        name='Main Shop',
        address='Central Street 1',
    )

    app_state.sales_points.append(
        sales_point
    )

    DatabaseManager.add_sales_point(
        sales_point
    )

    return sales_point


def get_sales_point(app_state):
    """Получение точки продаж."""

    if not app_state.sales_points:

        return create_first_sales_point(
            app_state
        )

    return app_state.sales_points[0]


def load_products_to_sales_point(
    sales_point,
):
    """Загрузка товаров."""

    products = (
        DatabaseManager.load_products()
    )

    sales_point.products = products


def show_sales_point_info(app_state):
    """Показ информации о точке."""

    ConsoleManager.header(
        'ТОЧКА ПРОДАЖ'
    )

    if not app_state.sales_points:

        print('Точек продаж нет.')

        ConsoleManager.pause()

        return

    for sales_point in app_state.sales_points:

        print(sales_point.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def show_products(app_state):
    """Показ товаров."""

    ConsoleManager.header(
        'ТОВАРЫ'
    )

    sales_point = select_sales_point(
        app_state
    )

    if not sales_point:

        return

    load_products_to_sales_point(
        sales_point
    )

    if not sales_point.products:

        print('Товаров нет.')

        ConsoleManager.pause()

        return

    for product in sales_point.products:

        print(product.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def create_order(app_state):
    """Создание заказа."""

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ ЗАКАЗА'
        )

        sales_point = select_sales_point(
            app_state
        )

        if not sales_point:

            return

        if not sales_point.is_opened:

            print(
                'Точка продаж закрыта.'
            )

            ConsoleManager.pause()

            return

        users = DatabaseManager.load_users()

        customers = [
            user
            for user in users
            if isinstance(user, Customer)
        ]

        if not customers:

            print(
                'Покупателей нет.'
            )

            ConsoleManager.pause()

            return

        print('ПОКУПАТЕЛИ:\n')

        for customer in customers:

            print(customer.get_info())

            print('-' * 50)

        customer_id = int(
            input(
                '\nВведите ID покупателя: '
            )
        )

        customer = next(
            (
                customer
                for customer in customers
                if (
                    customer.user_id
                    == customer_id
                )
            ),
            None,
        )

        if not customer:

            raise ValueError(
                'Покупатель не найден.'
            )

        order = (
            SalesActions.create_order(
                customer
            )
        )

        app_state.current_orders.append(
            order
        )

        print(
            '\nЗаказ успешно создан.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def show_current_order(app_state):
    """Показ текущего заказа."""

    ConsoleManager.header(
        'ТЕКУЩИЙ ЗАКАЗ'
    )

    if not app_state.current_orders:

        print('Заказов нет.')

        ConsoleManager.pause()

        return

    order = (
        app_state.current_orders[-1]
    )

    print(order.get_info())

    print('-' * 50)

    if not order.products:

        print('Товаров в заказе нет.')

        ConsoleManager.pause()

        return

    for product in order.products:

        print(product.get_info())

        print('-' * 30)

    ConsoleManager.pause()


def add_product_to_order(app_state):
    """Добавление товара в заказ."""

    try:

        ConsoleManager.header(
            'ДОБАВЛЕНИЕ ТОВАРА'
        )

        if not app_state.current_orders:

            print(
                'Сначала создайте заказ.'
            )

            ConsoleManager.pause()

            return

        sales_point = select_sales_point(
            app_state
        )

        if not sales_point:

            return

        load_products_to_sales_point(
            sales_point
        )

        if not sales_point.products:

            print('Товаров нет.')

            ConsoleManager.pause()

            return

        order = (
            app_state.current_orders[-1]
        )

        print('ТОВАРЫ:\n')

        for product in sales_point.products:

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

        (
            SalesActions
            .add_product_to_order(
                sales_point=sales_point,
                order=order,
                product_id=product_id,
                quantity=quantity,
            )
        )

        print(
            '\nТовар успешно добавлен.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def sell_order(app_state):
    """Продажа заказа."""

    try:

        ConsoleManager.header(
            'ПРОДАЖА ЗАКАЗА'
        )

        if not app_state.current_orders:

            print('Заказов нет.')

            ConsoleManager.pause()

            return

        sales_point = select_sales_point(
            app_state
        )

        if not sales_point:

            return

        order = (
            app_state.current_orders[-1]
        )

        if not order.products:

            print(
                'В заказе нет товаров.'
            )

            ConsoleManager.pause()

            return

        (
            SalesActions
            .sell_products(
                sales_point=sales_point,
                order=order,
            )
        )

        DatabaseManager.add_order(
            order
        )

        print(
            '\nПродажа успешно выполнена.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def return_order(app_state):
    """Возврат заказа."""

    try:

        ConsoleManager.header(
            'ВОЗВРАТ ЗАКАЗА'
        )

        orders = (
            DatabaseManager.load_orders()
        )

        if not orders:

            print('Заказов нет.')

            ConsoleManager.pause()

            return

        for order in orders:

            print(order.get_info())

            print('-' * 50)

        order_id = int(
            input(
                '\nВведите ID заказа: '
            )
        )

        order = next(
            (
                order
                for order in orders
                if (
                    order.order_id
                    == order_id
                )
            ),
            None,
        )

        if not order:

            raise ValueError(
                'Заказ не найден.'
            )

        sales_point = select_sales_point(
            app_state
        )

        if not sales_point:

            return

        (
            SalesActions
            .return_products(
                sales_point=sales_point,
                order=order,
            )
        )

        print(
            '\nВозврат успешно выполнен.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def show_orders():
    """Показ заказов."""

    ConsoleManager.header(
        'ЗАКАЗЫ'
    )

    orders = (
        DatabaseManager.load_orders()
    )

    if not orders:

        print('Заказов нет.')

        ConsoleManager.pause()

        return

    for order in orders:

        print(order.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def open_sales_point(app_state):
    """Открытие точки продаж."""

    ConsoleManager.header(
        'ОТКРЫТИЕ ТОЧКИ'
    )

    sales_point = select_sales_point(
        app_state
    )

    if not sales_point:

        return

    sales_point.open()

    DatabaseManager.update_sales_point(
        sales_point
    )

    print(
        'Точка продаж открыта.'
    )

    ConsoleManager.pause()


def close_sales_point(app_state):
    """Закрытие точки продаж."""

    ConsoleManager.header(
        'ЗАКРЫТИЕ ТОЧКИ'
    )

    sales_point = select_sales_point(
        app_state
    )

    if not sales_point:

        return

    sales_point.close()

    DatabaseManager.update_sales_point(
        sales_point
    )

    print(
        'Точка продаж закрыта.'
    )

    ConsoleManager.pause()


def sales_menu(app_state):
    """Меню продаж."""

    while True:

        ConsoleManager.header(
            'ПРОДАЖИ'
        )

        print('1. Информация о точке продаж')

        print('2. Показать товары')

        print('3. Создать заказ')

        print(
            '4. Добавить товар в заказ'
        )

        print(
            '5. Показать текущий заказ'
        )

        print('6. Продать заказ')

        print('7. Возврат заказа')

        print('8. Показать заказы')

        print(
            '9. Открыть точку продаж'
        )

        print(
            '10. Закрыть точку продаж'
        )

        print('11. Создать точку продаж')

        print('12. Добавить сотрудника в точку')

        print('13. Показать сотрудников в точке')

        print('14. Удалить сотрудника из точки')

        print('15. Назад')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                show_sales_point_info(
                    app_state
                )

            case '2':

                show_products(app_state)

            case '3':

                create_order(app_state)

            case '4':

                add_product_to_order(
                    app_state
                )

            case '5':

                show_current_order(
                    app_state
                )

            case '6':

                sell_order(app_state)

            case '7':

                return_order(app_state)

            case '8':

                show_orders()

            case '9':

                open_sales_point(
                    app_state
                )

            case '10':

                close_sales_point(
                    app_state
                )

            case '11':

                create_sales_point_menu(
                    app_state
                )

            case '12':

                add_employee_to_sales_point(
                    app_state
                )

            case '13':

                show_employees_in_sales_point(
                    app_state
                )

            case '14':

                remove_employee_from_sales_point(
                    app_state
                )

            case '15':

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()


def create_sales_point_menu(app_state):
    """Меню создания точки продаж."""

    try:

        ConsoleManager.header(
            'СОЗДАНИЕ ТОЧКИ ПРОДАЖ'
        )

        name = input('Название точки: ')

        address = input('Адрес: ')

        warehouses = DatabaseManager.load_warehouses()

        if not warehouses:

            print('\nВНИМАНИЕ: Складов нет. Сначала создайте склад.')

            ConsoleManager.pause()

            return

        print('\nСКЛАДЫ:\n')

        for warehouse in warehouses:

            print(
                f'{warehouse.warehouse_id}. '
                f'{warehouse.name} - '
                f'{warehouse.address}'
            )

        warehouse_id = int(
            input(
                '\nВведите ID склада для привязки: '
            )
        )

        warehouse = next(
            (
                wh
                for wh in warehouses
                if wh.warehouse_id == warehouse_id
            ),
            None,
        )

        if not warehouse:

            raise ValueError(
                'Склад не найден.'
            )

        sales_point = SalesPoint(
            name=name,
            address=address,
            warehouse_id=warehouse.warehouse_id,
        )

        app_state.sales_points.append(
            sales_point
        )

        DatabaseManager.add_sales_point(
            sales_point
        )

        print(
            '\nТочка продаж успешно создана и привязана к складу.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def add_employee_to_sales_point(app_state):
    """Добавление сотрудника в точку продаж."""

    try:

        ConsoleManager.header(
            'ДОБАВЛЕНИЕ СОТРУДНИКА В ТОЧКУ ПРОДАЖ'
        )

        if not app_state.sales_points:

            print('Точек продаж нет.')

            ConsoleManager.pause()

            return

        users = DatabaseManager.load_users()

        employees = [
            user
            for user in users
            if isinstance(user, Employee)
            and user.is_working
        ]

        if not employees:

            print('Сотрудников нет.')

            ConsoleManager.pause()

            return

        print('ТОЧКИ ПРОДАЖ:\n')

        for sales_point in app_state.sales_points:

            print(
                f'{sales_point.sales_point_id}. '
                f'{sales_point.name} - '
                f'{sales_point.address}'
            )

            print('-' * 50)

        sales_point_id = int(
            input(
                '\nВведите ID точки продаж: '
            )
        )

        sales_point = get_sales_point_by_id(
            app_state,
            sales_point_id,
        )

        print('\nСОТРУДНИКИ:\n')

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
                emp
                for emp in employees
                if emp.user_id == employee_id
            ),
            None,
        )

        if not employee:

            raise ValueError(
                'Сотрудник не найден.'
            )

        sales_point.add_employee(employee)

        DatabaseManager.update_sales_point(
            sales_point
        )

        print(
            '\nСотрудник успешно добавлен в точку продаж.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()


def show_employees_in_sales_point(app_state):
    """Показ сотрудников в точке продаж."""

    ConsoleManager.header(
        'СОТРУДНИКИ В ТОЧКЕ ПРОДАЖ'
    )

    sales_point = select_sales_point(
        app_state
    )

    if not sales_point:

        return

    if not sales_point.employees:

        print('В точке продаж нет сотрудников.')

        ConsoleManager.pause()

        return

    print(f'Точка продаж: {sales_point.name}\n')

    for employee in sales_point.employees:

        print(employee.get_info())

        print('-' * 50)

    ConsoleManager.pause()


def remove_employee_from_sales_point(app_state):
    """Удаление сотрудника из точки продаж."""

    try:

        ConsoleManager.header(
            'УДАЛЕНИЕ СОТРУДНИКА ИЗ ТОЧКИ ПРОДАЖ'
        )

        sales_point = select_sales_point(
            app_state
        )

        if not sales_point:

            return

        if not sales_point.employees:

            print('В точке продаж нет сотрудников.')

            ConsoleManager.pause()

            return

        print('СОТРУДНИКИ:\n')

        for employee in sales_point.employees:

            print(employee.get_info())

            print('-' * 50)

        employee_id = int(
            input(
                '\nВведите ID сотрудника для удаления: '
            )
        )

        sales_point.remove_employee(employee_id)

        DatabaseManager.update_sales_point(
            sales_point
        )

        print(
            '\nСотрудник успешно удален из точки продаж.'
        )

    except ValueError as error:

        print(f'\nОшибка: {error}')

    ConsoleManager.pause()