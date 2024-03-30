LOGS_FILENAME = "logs.txt"
CONFIG_FILE_NAME = "config.json"
DB_FILE_NAME = "db.sqlite"
EXCLUDED_CONFIG_KEYS_FOR_SAVE = (
    "db_cursor",
    "db_connection",
)

INITIAL_TRANSACTION_DESCRIPTION = "Начальное значение счета"
ACCOUNT_TRANSACTIONS_LIMIT_TO_SELECT = 100
SELECT_LIST_TABULAR_SEPARATOR = "\t\t\t\t"

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
UI_ACCOUNTS_SCREEN_LABEL_MESSAGE = "Работа с вашими вирутальными счетами"
UI_ADD_ACCOUNT_LABEL_MESSAGE = "Введите название виртуального счета"
UI_ADD_ACCOUNT_BUTTON_MESSAGE = "Создать новый виртуальный счет"
UI_ADD_ACCOUNT_INPUT_PLACEHOLDER = "Название виртуального счета"
UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE = "Начальное виртуального значение счета"
UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE = (
    "Некорректное название виртуального счета " "или счет с таким названием уже существует"
)
UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE = "Некорректное числовое значение"
UI_BUTTON_OK_LABEL = "OK"
UI_ALL_ACCOUNTS_SELECT_TITLE = "Виртуальные счета"
UI_ACCOUNT_TRANSACTIONS_TITLE = "Последние транзакции по счету"
UI_ADD_TRANSACTION_LABEL_MESSAGE = "Добавление транзакции"
UI_ADD_TRANSACTION_AMOUNT_INPUT_PLACEHOLDER = "Сумма операции"
UI_ADD_TRANSACTION_DESCRIPTION_INPUT_PLACEHOLDER = "Описание операции"
UI_CATEGORY_EXPENSE_LABEL = "Расход"
UI_CATEGORY_INCOME_LABEL = "Приход"
UI_CATEGORY_TRANSFER_LABEL = "Перевод между счетами"
UI_SELECT_CATEGORY_LIST_PLACEHOLDER = "Выберите категорию"
UI_SELECT_ACCOUNT_TRANSER_LIST_PLACEHOLDER = "Счет, на который осуществить перевод"
UI_BAD_CATEGORY_LABEL_MESSAGE = "Категория либо не выбрана, либо некорректна"
