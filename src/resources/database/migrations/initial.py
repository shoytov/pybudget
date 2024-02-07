from src.resources.database.migrations.base import BaseMigration
from src.utils.decorators import transaction_decorator


class InitialMigration(BaseMigration):
    name = "initial"
    number = 0

    @transaction_decorator
    def execute(self):  # type: ignore
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS migrations
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT not null,
            created_at INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS migrations_name_uindex ON migrations (name);
            """
        )
