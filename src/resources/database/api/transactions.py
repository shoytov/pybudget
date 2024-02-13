from decimal import Decimal
from time import time

from src.accounting.enums import TransactionType
from src.resources.core import CONFIG
from src.utils.decorators import transaction_decorator


class TransactionsApi:
    @transaction_decorator
    def add_transaction(
        self, account_id: int, transaction_type: TransactionType, amount: Decimal, description: str
    ) -> None:
        query = (
            "INSERT INTO transactions (type, value, account_id, description, created_at)"
            "VALUES (?, ?, ?, ?, ?);"
        )
        CONFIG.db_cursor.execute(  # type: ignore
            query, (transaction_type, amount, account_id, description, int(time()))
        )
