from src.resources.config.manager import ConfigManager
from src.resources.core import CONFIG
from src.resources.database.manager import DatabaseManager


class DownResources:
    def __init__(self) -> None:
        # ConfigManager.save_config(CONFIG.value)
        DatabaseManager.close_connection()
