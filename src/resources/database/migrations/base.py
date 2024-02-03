from abc import ABC, abstractmethod


class BaseMigration(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_sql_from_file(self) -> str:
        pass
