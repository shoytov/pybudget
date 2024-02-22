from decimal import Decimal
from sqlite3 import Row
from time import time

from src.accounting.enums import TransactionType
from src.consts import ACCOUNT_TRANSACTIONS_LIMIT_TO_SELECT
from src.resources.core import CONFIG
from src.utils.decorators import transaction_decorator


class TransactionsApi:
    @transaction_decorator
    def add_transaction(
        self,
        account_id: int,
        category_id: int,
        transaction_type: TransactionType,
        amount: Decimal,
        description: str,
    ) -> None:
        query = (
            "INSERT INTO transactions "
            "(type, value, account_id, category_id, description, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?);"
        )
        CONFIG.db_cursor.execute(  # type: ignore
            query, (transaction_type, amount, account_id, category_id, description, int(time()))
        )

    @classmethod
    def get_account_transactions(cls, account_id: int) -> list[Row] | list:
        query = (
            "SELECT transactions.id as id, transactions.type as type, "
            "transactions.value as value, transactions.account_id as account_id, "
            "transactions.category_id as category_id, transactions.description as description, "
            "transactions.created_at as created_at, categories.name as category_name, "
            "categories.icon as category_icon "
            "FROM transactions INNER JOIN categories ON transactions.category_id = categories.id "
            "WHERE transactions.account_id = ? ORDER BY created_at DESC LIMIT ?"
        )

        CONFIG.db_cursor.execute(  # type: ignore
            query, (account_id, ACCOUNT_TRANSACTIONS_LIMIT_TO_SELECT)
        )
        transactions = CONFIG.db_cursor.fetchall()  # type: ignore
        return transactions
