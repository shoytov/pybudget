from abc import ABC, abstractmethod
from time import time
from sqlite3 import Cursor

from src.resources.core import CONFIG


class BaseMigration(ABC):
    def __init__(self) -> None:
        if CONFIG.db_cursor is not None:
            self.cursor: Cursor = CONFIG.db_cursor
        else:
            raise ValueError("Cursor is None")

    def _add_migration(self, migration_name: str) -> None:
        self.cursor.execute(
            "INSERT INTO migrations (name, created) values (?, ?);",
            (migration_name, str(int(time()))),
        )

    @abstractmethod
    def execute(self):
        pass
