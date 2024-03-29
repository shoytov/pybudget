from sqlite3 import Connection, Cursor


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
        self._value["db_path"] = path

    @property
    def db_connection(self) -> Connection | None:
        return self._value.get("db_connection")

    @db_connection.setter
    def db_connection(self, value: Connection) -> None:
        self._value["db_connection"] = value

    @db_connection.deleter
    def db_connection(self) -> None:
        del self._value["db_connection"]

    @property
    def db_cursor(self) -> Cursor | None:
        return self._value.get("db_cursor")

    @db_cursor.setter
    def db_cursor(self, cursor: Cursor) -> None:
        self._value["db_cursor"] = cursor

    @db_cursor.deleter
    def db_cursor(self) -> None:
        del self._value["db_cursor"]


CONFIG = Config.get_instance()
