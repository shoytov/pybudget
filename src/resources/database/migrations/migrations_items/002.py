from src.resources.database.migrations.base import BaseMigration
from src.utils.decorators import transaction_decorator


class CategoriesDataMigration(BaseMigration):
    name = "002.py"
    number = 2

    @transaction_decorator
    def execute(self):  # type: ignore
        data_for_insert = (
            # category
            (1, "Автомобиль", "🚗", None, False),
            (2, "Стоянка", "🚏", 1, False),
            (3, "Страховка", "📃", 1, False),
            (4, "Обслуживание", "🛠️", 1, False),
            (5, "Аксессуары", "🧰", 1, False),
            (6, "Топливо", "⛽", 1, False),
            (7, "Другое", "❓", 1, False),
            # category
            (8, "Общественный транспорт", "🚋", None, False),
            # category
            (9, "Питание", "🍔", None, False),
            (10, "Бакалея", "🍗", 9, False),
            (11, "Ресторан", "🍿", 9, False),
            (12, "Алкоголь", "🍹", 9, False),
            (13, "Питание (другое)", "🍳", 9, False),
            # category
            (14, "Жилище", "🏠", None, False),
            (15, "Мебель/аксессуары", "🛋️", 14, False),
            (16, "Обслуживание/ремонт", "🪚", 14, False),
            (17, "Жилище (другое)", "🛁", 14, False),
            # category
            (18, "Здоровье", "🩻", None, False),
            (19, "Лекарства", "💊", 18, False),
            (20, "Медицина", "🩺", 18, False),
            (21, "Стоматология", "🦷", 18, False),
            # category
            (22, "Счета", "📜", None, False),
            (23, "Налоги", "💸", 22, False),
            (24, "ЖКХ", "📨", 22, False),
            (25, "Ипотека", "🏛️", 22, False),
            (26, "Телефон/Интернет", "☎️", 22, False),
            (27, "Другие счета", "💹", 22, False),
            # category
            (28, "Подарки", "🎁", None, False),
            # category
            (29, "Досуг/Хобби", "🥳", None, False),
            # category
            (30, "Ребенок", "👶", None, False),
            # category
            (31, "Путешествия", "✈️", None, False),
            # category
            (32, "Другие расходы", "📝", None, False),
            # category
            (33, "Одежда/Обувь/Аксессуары", "👠", None, False),
            (34, "Одежда", "👔", 33, False),
            (35, "Обувь", "👢", 33, False),
            (36, "Аксессуары", "🧣", 33, False),
            (37, "Ремонт", "🪡", 33, False),
            # category
            (38, "Бытовая химия", "🧴", None, False),
            # category
            (39, "Питомец", "🦥", None, False),
            # category
            (40, "Зарплата", "💰", None, True),
            # category
            (41, "Дополнительный доход (подработка)", "💵", None, True),
            # category
            (42, "Инвестиции", "🪙", None, True),
            # category
            (43, "Подарочные деньги", "👛", None, True),
        )
        self.cursor.executemany(
            """
            INSERT INTO categories (id, name, icon, parent_id, is_income) VALUES (?, ?, ?, ?, ?);
            """,
            data_for_insert,
        )
        self._add_migration(self.name)
