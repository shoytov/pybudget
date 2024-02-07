from src.resources.database.migrations.base import BaseMigration
from src.utils.decorators import transaction_decorator


class CategoriesMigration(BaseMigration):
    name = "001.py"
    number = 1

    @transaction_decorator
    def execute(self):  # type: ignore
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS categories
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT not null,
            icon TEXT,
            parent_id INTEGER,
            is_income BOOLEAN NOT NULL CHECK (is_income IN (0, 1)));
            CREATE UNIQUE INDEX IF NOT EXISTS categories_name_uindex ON categories (name);
        """
        )
        self._add_migration(self.name)
