"""База данных - Менеджер базы данных."""

from core.database.json_manager import (
    JsonManager,
)
from core.products.model import Product
from core.sales.order import Order
from core.sales.sales_point import (
    SalesPoint,
)
from core.users.customer.model import (
    Customer,
)
from core.users.employee.model import (
    Employee,
)
from core.warehouse.warehouse import (
    Warehouse,
)


class DatabaseManager:
    """Менеджер базы данных."""

    DATABASE_PATH = (
        'core/database/data.json'
    )

    @classmethod
    def load_database(cls) -> dict:
        """Загрузка базы данных."""

        return JsonManager.load_data(
            cls.DATABASE_PATH
        )

    @classmethod
    def save_database(
        cls,
        data: dict,
    ):
        """Сохранение базы данных."""

        JsonManager.save_data(
            cls.DATABASE_PATH,
            data,
        )

    @staticmethod
    def find_user_by_id(
        users: list,
        user_id: int,
    ):
        """Поиск пользователя."""

        for user in users:

            if user.user_id == user_id:

                return user

        raise ValueError(
            'Пользователь не найден.'
        )

    @classmethod
    def add_user(
        cls,
        user,
    ):
        """Добавление пользователя."""

        data = cls.load_database()

        data['users'].append(
            user.to_dict()
        )

        cls.save_database(data)

    @classmethod
    def update_user(
        cls,
        updated_user,
    ):
        """Обновление пользователя."""

        data = cls.load_database()

        for index, user_data in enumerate(
            data['users']
        ):

            if (
                user_data['user_id']
                == updated_user.user_id
            ):

                data['users'][index] = (
                    updated_user.to_dict()
                )

                break

        cls.save_database(data)

    @classmethod
    def add_product(
        cls,
        product: Product,
    ):
        """Добавление товара."""

        data = cls.load_database()

        data['products'].append(
            product.to_dict()
        )

        cls.save_database(data)

    @classmethod
    def update_product(
        cls,
        updated_product: Product,
    ):
        """Обновление товара."""

        data = cls.load_database()

        for index, product_data in enumerate(
            data['products']
        ):

            if (
                product_data['product_id']
                == updated_product.product_id
            ):

                data['products'][index] = (
                    updated_product.to_dict()
                )

                break

        cls.save_database(data)

    @classmethod
    def load_products(cls):
        """Загрузка товаров."""

        data = cls.load_database()

        return [
            Product.from_dict(product)
            for product in data['products']
        ]

    @classmethod
    def add_warehouse(
        cls,
        warehouse: Warehouse,
    ):
        """Добавление склада."""

        data = cls.load_database()

        data['warehouses'].append(
            warehouse.to_dict()
        )

        cls.save_database(data)

    @classmethod
    def update_warehouse(
        cls,
        updated_warehouse,
    ):
        """Обновление склада."""

        data = cls.load_database()

        for index, warehouse_data in enumerate(
            data['warehouses']
        ):

            if (
                warehouse_data['warehouse_id']
                == updated_warehouse.warehouse_id
            ):

                data['warehouses'][index] = (
                    updated_warehouse.to_dict()
                )

                break

        cls.save_database(data)

    @classmethod
    def load_warehouses(cls):
        """Загрузка складов."""

        data = cls.load_database()

        users = cls.load_users()

        warehouses = []

        for warehouse_data in data[
            'warehouses'
        ]:

            manager = cls.find_user_by_id(
                users,
                warehouse_data['manager_id'],
            )

            warehouse = Warehouse.from_dict(
                warehouse_data,
                manager,
            )

            warehouses.append(warehouse)

        return warehouses

    @classmethod
    def add_sales_point(
        cls,
        sales_point: SalesPoint,
    ):
        """Добавление точки продаж."""

        data = cls.load_database()

        sp_dict = sales_point.to_dict()
        

        if hasattr(sales_point, 'warehouse_id') and sales_point.warehouse_id:
            sp_dict['warehouse_id'] = sales_point.warehouse_id
        
        data['sales_points'].append(
            sp_dict
        )

        cls.save_database(data)

    @classmethod
    def update_sales_point(
        cls,
        updated_sales_point: SalesPoint,
    ):
        """Обновление точки продаж."""

        data = cls.load_database()

        for index, sp_data in enumerate(
            data['sales_points']
        ):

            if (
                sp_data['sales_point_id']
                == updated_sales_point.sales_point_id
            ):

                sp_dict = updated_sales_point.to_dict()
                

                if hasattr(updated_sales_point, 'warehouse_id'):
                    sp_dict['warehouse_id'] = updated_sales_point.warehouse_id
                
                data['sales_points'][index] = sp_dict

                break

        cls.save_database(data)

    @classmethod
    def load_sales_points(cls):
        """Загрузка точек продаж."""

        data = cls.load_database()

        users = cls.load_users()

        sales_points = []

        for sp_data in data['sales_points']:

            employees = [
                user for user in users
                if user.user_id in sp_data.get('employees', [])
            ]

            sales_point = SalesPoint.from_dict(
                sp_data,
                employees,
            )
            

            if 'warehouse_id' in sp_data:
                sales_point.warehouse_id = sp_data['warehouse_id']

            sales_points.append(sales_point)

        return sales_points

    @classmethod
    def add_order(
        cls,
        order: Order,
    ):
        """Добавление заказа."""

        data = cls.load_database()

        data['orders'].append(
            order.to_dict()
        )

        cls.save_database(data)

    @classmethod
    def update_order(
        cls,
        updated_order,
    ):
        """Обновление заказа."""

        data = cls.load_database()

        for index, order_data in enumerate(
            data['orders']
        ):

            if (
                order_data['order_id']
                == updated_order.order_id
            ):

                data['orders'][index] = (
                    updated_order.to_dict()
                )

                break

        cls.save_database(data)

    @classmethod
    def load_orders(cls):
        """Загрузка заказов."""

        data = cls.load_database()

        users = cls.load_users()

        orders = []

        for order_data in data['orders']:

            customer = cls.find_user_by_id(
                users,
                order_data['customer_id'],
            )

            order = Order.from_dict(
                order_data,
                customer,
            )

            orders.append(order)

        return orders

    @classmethod
    def load_users(cls):
        """Загрузка пользователей."""

        data = cls.load_database()

        users = []

        for user_data in data['users']:

            if (
                user_data['user_type']
                == 'employee'
            ):

                users.append(
                    Employee.from_dict(
                        user_data
                    )
                )

            elif (
                user_data['user_type']
                == 'customer'
            ):

                users.append(
                    Customer.from_dict(
                        user_data
                    )
                )

        return users

    @classmethod
    def clear_database(cls):
        """Очистка базы данных."""

        from core.utils.generators import IdGenerator
        
        data = {
            'users': [],
            'products': [],
            'warehouses': [],
            'sales_points': [],
            'orders': [],
        }

        cls.save_database(data)
        

        IdGenerator.reset_all()

    @classmethod
    def create_demo_data(cls):
        """Создание демонстрационных данных."""

        from core.users.employee.model import Employee
        from core.users.customer.model import Customer
        from core.products.model import Product
        from core.products.enums import ProductCategory
        from core.warehouse.warehouse import Warehouse
        from core.sales.sales_point import SalesPoint
        from core.users.base_user.address import Address
        from core.users.base_user.enums import Gender
        from core.users.base_user.enums import EmployeeRole
        from datetime import date


        cls.clear_database()


        manager = Employee(
            first_name='Иван',
            last_name='Иванов',
            birth_date=date(1990, 1, 1),
            gender=Gender.MALE,
            phone='+79991234567',
            email='ivan@example.com',
            address=Address(
                country='Россия',
                city='Москва',
                street='Тверская',
                house_number='1',
                postal_code='101000',
            ),
            role=EmployeeRole.MANAGER,
            salary=100000.0,
        )

        cls.add_user(manager)


        seller = Employee(
            first_name='Петр',
            last_name='Петров',
            birth_date=date(1995, 5, 15),
            gender=Gender.MALE,
            phone='+79997654321',
            email='petr@example.com',
            address=Address(
                country='Россия',
                city='Москва',
                street='Пушкина',
                house_number='10',
                postal_code='101001',
            ),
            role=EmployeeRole.SELLER,
            salary=80000.0,
        )

        cls.add_user(seller)


        customer = Customer(
            first_name='Анна',
            last_name='Смирнова',
            birth_date=date(1988, 3, 20),
            gender=Gender.FEMALE,
            phone='+79991112233',
            email='anna@example.com',
            address=Address(
                country='Россия',
                city='Санкт-Петербург',
                street='Невский',
                house_number='50',
                postal_code='190000',
            ),
        )

        cls.add_user(customer)


        products = [
            Product(
                name='Яблоки',
                category=ProductCategory.FOOD,
                price=150.0,
                quantity=100,
            ),
            Product(
                name='Ноутбук',
                category=ProductCategory.ELECTRONICS,
                price=75000.0,
                quantity=20,
            ),
            Product(
                name='Футболка',
                category=ProductCategory.CLOTHES,
                price=1500.0,
                quantity=50,
            ),
            Product(
                name='Диван',
                category=ProductCategory.FURNITURE,
                price=35000.0,
                quantity=10,
            ),
            Product(
                name='Хлеб',
                category=ProductCategory.FOOD,
                price=50.0,
                quantity=200,
            ),
        ]

        for product in products:
            cls.add_product(product)


        warehouse = Warehouse(
            name='Главный склад',
            address='г. Москва, ул. Складская, д. 1',
            manager=manager,
        )

        cls.add_warehouse(warehouse)


        sales_point = SalesPoint(
            name='Основной магазин',
            address='г. Москва, ул. Торговая, д. 5',
            warehouse_id=warehouse.warehouse_id,
        )

        cls.add_sales_point(sales_point)

        print('Демонстрационные данные успешно созданы!')
        print(f'  - Сотрудников: 2 (менеджер + продавец)')
        print(f'  - Покупателей: 1')
        print(f'  - Товаров: {len(products)}')
        print(f'  - Складов: 1')
        print(f'  - Точек продаж: 1')