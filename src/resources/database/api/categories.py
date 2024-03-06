from sqlite3 import Row

from src.resources.core import CONFIG


class CategoriesApi:
    @classmethod
    def get_all_categories(cls, is_income: bool | None = None) -> list[Row] | list:
        if is_income is not None:
            condition = "is_income=$1"
            params = (is_income,)
        else:
            condition = "1"
            params = ()

        query = f"SELECT * FROM categories WHERE {condition} order by name;"
        CONFIG.db_cursor.execute(query, params)  # type: ignore
        categories = CONFIG.db_cursor.fetchall()  # type: ignore
        return categories
