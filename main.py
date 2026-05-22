"""CRM Система - Точка входа."""

from core.database.database_manager import (
    DatabaseManager,
)
from core.warehouse.warehouse import Warehouse
from core.sales.sales_point import SalesPoint
from ui.main_menu import main_menu


def initialize_app_state():
    """Инициализация состояния приложения.

    Returns:
        Объект с состоянием приложения.
    """

    class AppState:
        """Состояние приложения."""

        def __init__(self):
            self.warehouses = []
            self.sales_points = []
            self.current_orders = []

    app_state = AppState()

    app_state.warehouses = (
        DatabaseManager.load_warehouses()
    )

    app_state.sales_points = (
        DatabaseManager.load_sales_points()
    )

    return app_state


def initialize_system():
    """Инициализация системы."""

    DatabaseManager.load_database()


def main():
    """Точка входа в программу."""

    try:

        print('\n=== CRM SYSTEM ===')
        print('1. Запустить систему')
        print('2. Очистить базу данных')
        print('3. Создать демонстрационные данные')

        choice = input('\nВыберите действие: ')

        if choice == '2':
            DatabaseManager.clear_database()
            print('\nБаза данных очищена.')
            return

        elif choice == '3':
            DatabaseManager.create_demo_data()
            print('\nДемонстрационные данные созданы.')

        initialize_system()

        app_state = (
            initialize_app_state()
        )

        print(
            'Система успешно запущена.'
        )

        main_menu(app_state)

    except KeyboardInterrupt:

        print(
            '\n\nПрограмма остановлена.'
        )

    except Exception as error:

        print(
            f'\nПроизошла ошибка: '
            f'{error}'
        )


if __name__ == '__main__':

    main()