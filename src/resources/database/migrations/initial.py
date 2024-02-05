from src.resources.database.migrations.base import BaseMigration


class InitialMigration(BaseMigration):
    name = "initial"
    number = 0

    def execute(self):
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS migrations
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT not null,
            created TEXT not null);
            CREATE UNIQUE INDEX IF NOT EXISTS migrations_name_uindex ON migrations (name);
        """
        )
