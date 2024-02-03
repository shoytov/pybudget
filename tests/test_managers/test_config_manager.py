import mock
import pytest

from src.resources.config.manager import ConfigManager


class TestConfigManager:
    @pytest.mark.parametrize("mock_result", (True, False))
    @mock.patch("src.utils.file_utils.check_file_exist")
    @mock.patch("src.utils.file_utils.create_file")
    def test_get_config(self, mock_create_file, mock_check_file_exist, mock_result):
        # Устанавливаем mock результат
        mock_check_file_exist.return_value = mock_result
        mock_create_file.return_value = None

        # Создаем mock для открытия файла
        mock_open = mock.mock_open(read_data='{"key": "value"}')

        # Заменяем функцию open на mock_open
        with mock.patch("builtins.open", mock_open):
            config_manager = ConfigManager()
            config = config_manager.get_config()

        # Проверяем, что результат соответствует ожидаемому
        assert config == {"key": "value"}
