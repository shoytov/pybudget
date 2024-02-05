from abc import ABC, abstractmethod
from sqlite3 import Cursor

from src.resources.core import CONFIG


class BaseMigration(ABC):
    def __init__(self) -> None:
        if CONFIG.db_cursor is not None:
            self.cursor: Cursor = CONFIG.db_cursor
        else:
            raise ValueError("Cursor is None")

    @abstractmethod
    def execute(self):
        pass
