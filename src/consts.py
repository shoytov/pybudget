LOGS_FILENAME = "logs.txt"
CONFIG_FILE_NAME = "config.json"
DB_FILE_NAME = "db.sqlite"
EXCLUDED_CONFIG_KEYS_FOR_SAVE = (
    "db_cursor",
    "db_connection",
)

# константы для текста в интерфейсе пользователя
UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE = (
    "Пусть к папке с базой данных не определен." "Необходимо его задать."
)
UI_DB_PATH_SET_BUTTON_MESSAGE = "Задать путь"
UI_DB_SET_LABEL_MESSAGE = "Выберите директорию, в которой будет храниться файл БД:"
