from abc import ABC, abstractmethod
from sqlite3 import Cursor
from time import time

from src.exceptions import DatabaseCursorNotExistError
from src.resources.core import CONFIG
from src.resources.database.api.migrations import MigrationsApi


class BaseMigration(ABC):
    def __init__(self) -> None:
        if CONFIG.db_cursor is not None:
            self.cursor: Cursor = CONFIG.db_cursor
        else:
            raise DatabaseCursorNotExistError

    def _add_migration(self, migration_name: str) -> None:
        MigrationsApi.add_migration(migration_name, int(time()))

    @abstractmethod
    def execute(self):
        pass
