LOGS_FILENAME = "logs.txt"
CONFIG_FILE_NAME = "config.json"
DB_FILE_NAME = "db.sqlite"
EXCLUDED_CONFIG_KEYS_FOR_SAVE = (
    "db_cursor",
    "db_connection",
)

INITIAL_TRANSACTION_DESCRIPTION = "Начальное значение счета"

# константы для текста в интерфейсе пользователя
UI_APP_TITLE = "PyBudget: персональный учет денежных средств"
UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE = (
    "Пусть к папке с базой данных не определен." "Необходимо его задать."
)
UI_DB_PATH_SET_BUTTON_MESSAGE = "Задать путь"
UI_DB_SET_LABEL_MESSAGE = "Выберите директорию, в которой будет храниться файл БД:"
UI_ADD_ACCOUNT_LABEL_TITLE = "Создание виртуального счета"
UI_NOT_ACCOUNTS_MESSAGE = (
    "Не добавлено ни одного вирутального счета. " "Для работы необходимо добавить хотя бы один счет"
)
UI_ADD_ACCOUNT_LABEL_MESSAGE = "Введите название виртуального счета"
UI_ADD_ACCOUNT_BUTTON_MESSAGE = "Создать новый виртуальный счет"
UI_ADD_ACCOUNT_INPUT_PLACEHOLDER = "Название виртуального счета"
UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE = "Начальное виртуального значение счета"
UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE = (
    "Некорректное название виртуального счета" "или счет с таким названием уже существует"
)
UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE = "Некорректное числовое значение"
UI_BUTTON_OK_LABEL = "OK"
