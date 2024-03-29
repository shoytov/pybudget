from src.resources.database.migrations.base import BaseMigration
from src.utils.decorators import transaction_decorator


class AccountsTransactionsTablesMigration(BaseMigration):
    name = "003.py"
    number = 3

    @transaction_decorator
    def execute(self):  # type: ignore
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            balance REAL DEFAULT 0);

            CREATE TABLE IF NOT EXISTS transactions
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            value REAL,
            account_id INTEGER REFERENCES accounts(id),
            category_id INTEGER REFERENCES categories(id),
            description TEXT,
            created_at INTEGER);

            CREATE INDEX IF NOT EXISTS accounts_id_idx ON transactions (account_id);
            CREATE INDEX IF NOT EXISTS category_id_idx ON transactions (category_id);
            CREATE INDEX IF NOT EXISTS transactions_type_idx ON transactions (type);
        """
        )
        self._add_migration(self.name)
