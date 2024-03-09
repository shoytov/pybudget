from decimal import Decimal

from loguru import logger
from pydantic import ValidationError

from src.accounting.enums import TransactionType
from src.accounting.managers.base import BaseMoneyManager
from src.accounting.managers.transactions import TransactionsManager
from src.accounting.models import Account
from src.consts import INITIAL_TRANSACTION_DESCRIPTION, SELECT_LIST_TABULAR_SEPARATOR
from src.exceptions import TransactionError
from src.resources.database.api.accounts import AccountsApi


class AccountsManager:
    @classmethod
    def get_all_accounts(
        cls, excluded_accounts_ids: tuple[int] | tuple = ()
    ) -> list[Account] | list:
        accounts = AccountsApi.get_all_accounts(excluded_accounts_ids)
        return [Account(**dict(account)) for account in accounts]

    @classmethod
    def get_formatted_accounts(cls) -> list[tuple[str, int]]:
        accounts = cls.get_all_accounts()
        return [  # type: ignore
            (
                f"{account.name} {SELECT_LIST_TABULAR_SEPARATOR} {account.balance}",
                account.account_id,
            )
            for account in accounts
        ]

    @classmethod
    def get_formatted_accounts_with_excluded(
        cls, excluded_accounts_ids: tuple[int] | tuple = ()
    ) -> list[tuple[int, str]]:
        return [  # type: ignore
            (f"{account.name}", account.account_id)
            for account in cls.get_all_accounts(excluded_accounts_ids)
        ]

    @classmethod
    def validate_account_name(cls, account_name: str) -> bool:
        if not account_name:
            return False
        accounts_counter = AccountsApi.get_same_accounts_by_name_count(account_name)
        return True if accounts_counter == 0 else False

    @classmethod
    def add_account(cls, account_name: str, inital_value: str) -> bool:
        balance = BaseMoneyManager.convert_amount_to_decimal(inital_value)
        try:
            new_account = Account(name=account_name, balance=balance)  # type: ignore
        except ValidationError as e:
            logger.error(e)
            return False
        try:
            account_id = AccountsApi().add_account(new_account)
        except TransactionError as e:
            logger.error(e)
            return False
        if balance > Decimal("0") and account_id is not None:
            return TransactionsManager.add_transaction(
                account_id, 44, TransactionType.INCOME, balance, INITIAL_TRANSACTION_DESCRIPTION
            )

        return True
