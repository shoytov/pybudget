import os
import sqlite3
from pathlib import Path

from src.consts import DB_FILE_NAME
from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG
from src.resources.database.migrations.initial import InitialMigration
from src.utils.file_utils import check_file_exist, create_file


class DatabaseManager:
    @classmethod
    def _get_full_db_path(cls) -> str:
        return os.path.join(CONFIG.db_path, DB_FILE_NAME)  # type: ignore

    @classmethod
    def _apply_migrations(cls) -> None:
        InitialMigration().execute()

    @classmethod
    def _set_db_connection(cls) -> None:
        connection = sqlite3.connect(cls._get_full_db_path())
        CONFIG.db_cursor = connection.cursor()

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
        ConfigManager.save_config(CONFIG.value)

        if cls.check_db_exist() is False:
            create_file(cls._get_full_db_path())

        cls._set_db_connection()
        cls._apply_migrations()

        return True
