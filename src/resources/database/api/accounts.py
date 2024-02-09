from sqlite3 import Row

from src.accounting.models import Account
from src.resources.core import CONFIG
from src.utils.decorators import transaction_decorator


class AccountsApi:
    @classmethod
    def get_all_accounts(cls) -> list[Row] | list:
        query = "SELECT * FROM accounts;"
        CONFIG.db_cursor.execute(query)  # type: ignore
        accounts = CONFIG.db_cursor.fetchall()  # type: ignore
        return accounts

    @transaction_decorator
    def add_account(self, account: Account) -> None:
        query = "INSERT INTO accounts (name, balance) VALUES (?, ?);"
        CONFIG.db_cursor.execute(query, (account.name, account.balance))  # type: ignore
