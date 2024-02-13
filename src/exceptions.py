class DatabaseInitializationError(ValueError):
    pass


class DatabaseConnectionNotExistError(ValueError):
    pass


class DatabaseCursorNotExistError(ValueError):
    pass


class TransactionError(ValueError):
    pass


class InvalidAmountError(ValueError):
    pass
