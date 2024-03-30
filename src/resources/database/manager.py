import importlib
import inspect
import os
import sqlite3
from decimal import Decimal
from pathlib import Path

from loguru import logger

from src.core.consts import DB_FILE_NAME
from src.exceptions import DatabaseConnectionNotExistError, DatabaseInitializationError
from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG
from src.resources.database.api.migrations import MigrationsApi
from src.resources.database.migrations.initial import InitialMigration
from src.utils.converters import adapter_decimal
from src.utils.file_utils import check_file_exist, create_file


class DatabaseManager:
    @classmethod
    def _get_full_db_path(cls) -> str:
        try:
            return os.path.join(CONFIG.db_path, DB_FILE_NAME)  # type: ignore
        except TypeError as e:
            logger.error(e)
            raise DatabaseInitializationError()

    @classmethod
    def _get_applied_migrations(cls) -> list[str] | list:
        applied_migrations = MigrationsApi.get_applied_migrations()
        result = []
        for migration in applied_migrations:
            result.append(dict(migration).get("name"))
        return result

    @classmethod
    def _get_migrations_for_apply(cls) -> list[str] | list:
        modules = os.listdir(
            os.path.join("src", "resources", "database", "migrations", "migrations_items")
        )
        res = [
            module[:-3]
            for module in modules
            if module not in cls._get_applied_migrations()
            and module != "__init__.py"
            and module != "__pycache__"
        ]
        return res

    @classmethod
    def _apply_migrations(cls) -> None:
        InitialMigration().execute()  # type: ignore

        new_migrations = cls._get_migrations_for_apply()

        for migration in new_migrations:
            module = importlib.import_module(
                f"src.resources.database.migrations.migrations_items.{migration}"
            )
            for _, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and hasattr(obj, "execute")
                    and not getattr(obj.execute, "__isabstractmethod__", False)
                ):
                    migration_instance = obj()
                    migration_instance.execute()

    @classmethod
    def _set_db_connection(cls) -> None:
        sqlite3.register_adapter(Decimal, adapter_decimal)
        connection = sqlite3.connect(cls._get_full_db_path(), isolation_level=None)
        connection.row_factory = sqlite3.Row
        CONFIG.db_connection = connection
        CONFIG.db_cursor = connection.cursor()

    @classmethod
    def close_connection(cls) -> None:
        try:
            CONFIG.db_cursor.close()  # type: ignore
        except AttributeError as e:
            logger.error(e)
            raise DatabaseConnectionNotExistError

    @classmethod
    def check_db_exist(cls) -> bool:
        return check_file_exist(cls._get_full_db_path())

    @classmethod
    def init_db(cls, db_path: str | Path | None) -> bool:
        """
        Создание файла базы данных и применение всех миграций.
        """
        if db_path is None:
            return False

        CONFIG.db_path = str(db_path)

        if cls.check_db_exist() is False:
            create_file(cls._get_full_db_path())
            ConfigManager.save_config(CONFIG.value)

        cls._set_db_connection()
        cls._apply_migrations()

        return True
