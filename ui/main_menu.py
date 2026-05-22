"""UI - Главное меню."""

from core.utils.console import (
    ConsoleManager,
)
from ui.customer_menu import (
    customer_menu,
)
from ui.employee_menu import (
    employee_menu,
)
from ui.product_menu import (
    product_menu,
)
from ui.sales_menu import (
    sales_menu,
)
from ui.warehouse_menu import (
    warehouse_menu,
)


def main_menu(app_state):
    """Главное меню."""

    while True:

        ConsoleManager.header(
            'CRM SYSTEM'
        )

        print('1. Товары')
        print('2. Склады')
        print('3. Продажи')
        print('4. Сотрудники')
        print('5. Покупатели')
        print('6. Выход')

        choice = input(
            '\nВыберите действие: '
        )

        match choice:

            case '1':

                product_menu()

            case '2':

                warehouse_menu(app_state)

            case '3':

                sales_menu(app_state)

            case '4':

                employee_menu(app_state)

            case '5':

                customer_menu(app_state)

            case '6':

                ConsoleManager.clear()

                print(
                    'Программа завершена.'
                )

                break

            case _:

                print(
                    '\nНеверный выбор.'
                )

                ConsoleManager.pause()