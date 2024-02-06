from src.resources.database.manager import DatabaseManager


class DownResources:
    def __init__(self) -> None:
        DatabaseManager.close_connection()
