from decimal import Decimal

from loguru import logger

from src.accounting.models import Transaction, TransactionType
from src.consts import SELECT_LIST_TABULAR_SEPARATOR
from src.exceptions import TransactionError
from src.resources.database.api.transactions import TransactionsApi


class TransactionsManager:
    @classmethod
    def add_transaction(
        cls,
        account_id: int,
        category_id: int,
        transaction_type: TransactionType,
        amount: str | int | float | Decimal,
        description: str,
    ) -> bool:
        try:
            TransactionsApi().add_transaction(
                account_id, category_id, transaction_type, amount, description
            )
            return True
        except TransactionError as e:
            logger.error(e)
            return False

    @classmethod
    def get_account_transactions(cls, account_id: str | int) -> list[Transaction]:
        transactions = TransactionsApi.get_account_transactions(int(account_id))
        return [Transaction(**dict(transaction)) for transaction in transactions]

    @classmethod
    def get_account_formatted_transactions(cls, account_id: str | int) -> list[tuple[str, int]]:
        transactions: list[Transaction] = cls.get_account_transactions(account_id)  # type: ignore
        return [  # type: ignore
            (
                f"{transaction.category_icon} {transaction.category_name} {SELECT_LIST_TABULAR_SEPARATOR} {transaction.value}",
                transaction.transaction_id,
            )
            for transaction in transactions
        ]
