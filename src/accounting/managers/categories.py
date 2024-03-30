from src.accounting.models import Category
from src.resources.database.api.categories import CategoriesApi


class CategoriesManager:
    @classmethod
    def get_all_categories(cls, is_income: bool | None = None) -> list[Category] | list:
        categories: list[Category] | list = CategoriesApi.get_all_categories(is_income)
        return [Category(**dict(category)) for category in categories]

    @classmethod
    def get_formatted_all_categories(cls, is_income: bool | None = None) -> list[tuple[int, str]]:
        return [  # type: ignore
            (f"{category.icon} {category.name}", category.category_id)
            for category in cls.get_all_categories(is_income)
        ]

    @classmethod
    def validate_category(cls, category_id: str | int, is_income: bool) -> bool:
        if not category_id:
            return False

        category: Category | None = CategoriesApi.get_category(category_id)

        if category is None:
            return False

        return category.is_income == is_income
