from decimal import Decimal

from pydantic import ValidationError

from src.accounting.models import Account
from src.exceptions import TransactionError
from src.resources.database.api.accounts import AccountsApi


class AccountsManager:
    @classmethod
    def get_all_accounts(cls) -> list[Account] | list:
        accounts = AccountsApi.get_all_accounts()
        return [Account(**dict(account)) for account in accounts]

    @classmethod
    def add_account(cls, account_name: str, inital_value: str) -> bool:
        try:
            new_account = Account(name=account_name, balance=Decimal(inital_value))  # type: ignore
        except ValidationError:
            return False
        try:
            AccountsApi().add_account(new_account)
        except TransactionError:
            return False

        return True
