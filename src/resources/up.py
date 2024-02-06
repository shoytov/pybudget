from loguru import logger

from src.consts import LOGS_FILENAME
from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG


class InitResources:
    def __init__(self) -> None:
        logger.add(LOGS_FILENAME)

        self._init_config()

    def _init_config(self) -> None:
        CONFIG.value = ConfigManager.get_config()
