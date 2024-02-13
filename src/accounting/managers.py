from decimal import Decimal, InvalidOperation

from loguru import logger
from pydantic import ValidationError

from src.accounting.enums import TransactionType
from src.accounting.models import Account
from src.consts import INITIAL_TRANSACTION_DESCRIPTION
from src.exceptions import InvalidAmountError, TransactionError
from src.resources.database.api.accounts import AccountsApi
from src.resources.database.api.transactions import TransactionsApi


class BaseMoneyManager:
    @classmethod
    def validate_amount(cls, value: str | int | float) -> bool:
        try:
            Decimal(value)
        except InvalidOperation:
            return False
        else:
            return True

    @classmethod
    def convert_amount_to_decimal(cls, value: str | int | float) -> Decimal:  # type: ignore
        try:
            result = Decimal(value)
        except InvalidOperation as e:
            logger.error(e)
            raise InvalidAmountError()
        else:
            return result


class TransactionsManager:
    @classmethod
    def add_transaction(
        cls,
        account_id: int,
        transaction_type: TransactionType,
        amount: str | int | float | Decimal,
        description: str,
    ) -> bool:
        try:
            TransactionsApi().add_transaction(account_id, transaction_type, amount, description)
            return True
        except TransactionError as e:
            logger.error(e)
            return False


class AccountsManager:
    @classmethod
    def get_all_accounts(cls) -> list[Account] | list:
        accounts = AccountsApi.get_all_accounts()
        return [Account(**dict(account)) for account in accounts]

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
                account_id, TransactionType.INCOME, balance, INITIAL_TRANSACTION_DESCRIPTION
            )

        return True
