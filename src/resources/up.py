from src.core.consts import LOGS_FILENAME
from src.core.logger import app_logger
from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG


class InitResources:
    def __init__(self) -> None:
        app_logger.add(LOGS_FILENAME)

        self._init_config()

    def _init_config(self) -> None:  # noqa
        CONFIG.value = ConfigManager.get_config()
