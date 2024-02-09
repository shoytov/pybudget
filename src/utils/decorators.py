from functools import wraps
from typing import Callable

from loguru import logger

from src.exceptions import TransactionError
from src.resources.core import CONFIG


def transaction_decorator(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            CONFIG.db_connection.commit()  # type: ignore
        except Exception as e:
            CONFIG.db_connection.rollback()  # type: ignore
            logger.error(e)
            raise TransactionError
        else:
            return result

    return wrapper
