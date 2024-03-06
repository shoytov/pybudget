from src.accounting.models import Category
from src.resources.database.api.categories import CategoriesApi


class CategoriesManager:
    @classmethod
    def get_all_categories(cls, is_income: bool | None = None) -> list[Category] | list:
        categories = CategoriesApi.get_all_categories(is_income)
        return [Category(**dict(category)) for category in categories]

    @classmethod
    def get_formatted_all_categories(cls, is_income: bool | None = None) -> list[tuple[int, str]]:
        return [  # type: ignore
            (f"{category.icon} {category.name}", category.category_id)
            for category in cls.get_all_categories(is_income)
        ]
