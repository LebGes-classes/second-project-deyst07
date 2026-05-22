"""База данных - JSON Менеджер."""

import json


class JsonManager:
    """Менеджер JSON."""

    @staticmethod
    def load_data(
        path: str,
    ) -> dict:
        """Загрузка данных."""

        try:

            with open(
                path,
                'r',
                encoding='utf-8',
            ) as file:

                return json.load(file)

        except FileNotFoundError:

            return {
                'users': [],
                'products': [],
                'warehouses': [],
                'sales_points': [],
                'orders': [],
            }

    @staticmethod
    def save_data(
        path: str,
        data: dict,
    ):
        """Сохранение данных."""

        with open(
            path,
            'w',
            encoding='utf-8',
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )