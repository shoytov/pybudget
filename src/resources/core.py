from src.resources.config.manager import ConfigManager


class Config:
    _instance = None
    _value = {}

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

    def __call__(self):
        return self.get_instance()

    @property
    def value(self) -> dict:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    @property
    def db_path(self) -> str | None:
        return self._value.get("db_path")

    @db_path.setter
    def db_path(self, path: str) -> None:
        self.value["db_path"] = path


CONFIG = Config.get_instance()


class InitResources:
    def __init__(self) -> None:
        self._init_config()

    def _init_config(self) -> None:
        global CONFIG

        CONFIG.value = ConfigManager.get_config()


class DownResources:
    def __init__(self) -> None:
        self._close_config()

    def _close_config(self) -> None:
        global CONFIG

        ConfigManager.save_config(CONFIG.value)
