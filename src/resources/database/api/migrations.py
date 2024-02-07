from sqlite3 import Row

from src.resources.core import CONFIG


class MigrationsApi:
    @classmethod
    def get_applied_migrations(cls) -> list[Row] | list:
        query = "SELECT name from migrations;"
        CONFIG.db_cursor.execute(query)  # type: ignore

        applied_migrations = CONFIG.db_cursor.fetchall()  # type: ignore
        return applied_migrations

    @classmethod
    def add_migration(cls, migration_name: str, created_at: int) -> None:
        query = "INSERT INTO migrations (name, created_at) values (?, ?);"
        CONFIG.db_cursor.execute(query, (migration_name, created_at))  # type: ignore
