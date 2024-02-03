import os
from pathlib import Path

from src.consts import DB_FILE_NAME
from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG
from src.utils.file_utils import check_file_exist, create_file


class DatabaseManager:
    @staticmethod
    def _get_full_db_path() -> str:
        return os.path.join(CONFIG.db_path, DB_FILE_NAME)  # type: ignore

    @staticmethod
    def check_db_exist() -> bool:
        return check_file_exist(DatabaseManager._get_full_db_path())

    @staticmethod
    def initial_migrations() -> None:
        pass

    @staticmethod
    def init_db(db_path: str | Path | None) -> bool:
        """
        Создание файла базы данных и применение всех миграций.
        """
        if db_path is None:
            return False

        CONFIG.db_path = str(db_path)
        ConfigManager.save_config(CONFIG.value)

        if DatabaseManager.check_db_exist() is False:
            create_file(DatabaseManager._get_full_db_path())
        return True
