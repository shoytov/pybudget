import orjson

from src.core.consts import CONFIG_FILE_NAME, EXCLUDED_CONFIG_KEYS_FOR_SAVE
from src.utils.file_utils import check_file_exist, create_file


class ConfigManager:
    @staticmethod
    def get_config() -> dict:
        if check_file_exist(CONFIG_FILE_NAME) is False:
            create_file(CONFIG_FILE_NAME)

        with open(CONFIG_FILE_NAME, "r") as settings_file:
            file_content: str = settings_file.read()

        try:
            config = orjson.loads(file_content)
        except orjson.JSONDecodeError:
            config = {}

        return config

    @staticmethod
    def save_config(config_data: dict) -> None:
        content_to_save = {
            key: value
            for key, value in config_data.items()
            if key not in EXCLUDED_CONFIG_KEYS_FOR_SAVE
        }

        with open(CONFIG_FILE_NAME, "wb") as settings_file:
            settings_file.write(orjson.dumps(content_to_save))
