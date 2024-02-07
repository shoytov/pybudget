from unittest.mock import patch

import pytest

from src.consts import DB_FILE_NAME
from src.exceptions import DatabaseInitializationError
from src.resources.core import CONFIG
from src.resources.database.manager import DatabaseManager


class TestDatabaseManager:
    @pytest.mark.parametrize("db_path", ("/home/user", None))
    def test__get_full_db_path(self, db_path):
        CONFIG.db_path = db_path

        if db_path is not None:
            result = DatabaseManager._get_full_db_path()
            assert isinstance(result, str)
            assert result == f"{db_path}/{DB_FILE_NAME}"
        else:
            with pytest.raises(DatabaseInitializationError):
                _ = DatabaseManager._get_full_db_path()

    @patch("src.resources.core.CONFIG.db_cursor")
    def test_get_applied_migrations_with_valid_db_cursor(self, mock_db_cursor):
        mock_db_cursor.execute.return_value = None
        mock_db_cursor.fetchall.return_value = [{"name": "migration_1"}, {"name": "migration_2"}]
        expected_migrations = ["migration_1", "migration_2"]
        result_migrations = DatabaseManager._get_applied_migrations()
        assert result_migrations == expected_migrations

    @pytest.mark.parametrize(
        "applied_migrations, expected_migrations",
        (([], ["migration_1", "migration_2"]), (["migration_1.py"], ["migration_2"])),
    )
    @patch("os.listdir")
    @patch("os.path.isfile")
    @patch.object(DatabaseManager, "_get_applied_migrations")
    def test_get_migrations_for_apply(
        self,
        mock_applied_migrations,
        mock_isfile,
        mock_listdir,
        applied_migrations,
        expected_migrations,
    ):
        mock_listdir.return_value = ["migration_1.py", "migration_2.py", "__init__.py"]
        mock_isfile.return_value = True
        mock_applied_migrations.return_value = applied_migrations

        migrations_for_apply = DatabaseManager._get_migrations_for_apply()

        assert migrations_for_apply == expected_migrations
