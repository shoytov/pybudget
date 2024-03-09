from sqlite3 import Row

from src.accounting.models import Account
from src.resources.core import CONFIG
from src.utils.decorators import transaction_decorator


class AccountsApi:
    @classmethod
    def get_all_accounts(cls, excluded_accounts_ids: tuple[int] | tuple = ()) -> list[Row] | list:
        if not excluded_accounts_ids:
            postfix = "1"
        else:
            excluded_ids = ",".join(map(str, excluded_accounts_ids))
            postfix = f"id NOT IN ({excluded_ids})"
        query = f"SELECT * FROM accounts WHERE {postfix};"
        CONFIG.db_cursor.execute(query)  # type: ignore
        accounts = CONFIG.db_cursor.fetchall()  # type: ignore
        return accounts

    @classmethod
    def get_same_accounts_by_name_count(cls, account_name: str) -> int:
        query = "SELECT COUNT(*) as counter from accounts where name=?"
        CONFIG.db_cursor.execute(query, (account_name,))  # type: ignore
        query_result = CONFIG.db_cursor.fetchone()  # type: ignore
        return dict(query_result).get("counter", 0)

    @transaction_decorator
    def add_account(self, account: Account) -> int | None:
        query = "INSERT INTO accounts (name, balance) VALUES (?, ?) RETURNING id;"
        CONFIG.db_cursor.execute(query, (account.name, account.balance))  # type: ignore
        row = CONFIG.db_cursor.fetchone()  # type: ignore
        return dict(row).get("id")
