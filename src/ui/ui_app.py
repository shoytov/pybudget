from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual_fspicker import SelectDirectory

from src.accounting.managers import AccountsManager
from src.consts import (
    UI_APP_TITLE,
    UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE,
    UI_DB_PATH_SET_BUTTON_MESSAGE,
    UI_DB_SET_LABEL_MESSAGE,
)
from src.exceptions import DatabaseInitializationError
from src.resources.core import CONFIG
from src.resources.database.manager import DatabaseManager
from src.ui.screens.accounts import AccountsScreen, AddAccountScreen, AccountScreen
from src.ui.screens.warnings import WarningScreenCommon


class BudgetApp(App):
    TITLE = UI_APP_TITLE
    BINDINGS = [
        Binding("q", "quit", "Quit", key_display="Q / CTRL+C"),
        Binding("Q", "quit", "Quit"),
    ]

    def show_selected_account_screen(self, account_id: str) -> None:
        self.push_screen(AccountScreen(account_id=account_id), callback=self.show_accounts_screen)

    def show_accounts_screen(self, _: bool) -> None:
        self.push_screen(AccountsScreen(), callback=self.show_selected_account_screen)

    def db_select_dir_callback(self, path: Path | None) -> None:
        result = DatabaseManager.init_db(path)
        if result is False:
            raise DatabaseInitializationError()
        self.push_screen(
            AddAccountScreen(is_first_account=True),
            callback=self.show_accounts_screen,  # type: ignore
        )

    def set_db_path_callback(self) -> None:
        self.push_screen(
            SelectDirectory(title=UI_DB_SET_LABEL_MESSAGE), callback=self.db_select_dir_callback
        )

    def on_ready(self) -> None:
        # если в конфиге отсутствует путь к файлу sqlite
        if not CONFIG.db_path:
            self.push_screen(
                WarningScreenCommon(
                    message_to_show=UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE,
                    button_label=UI_DB_PATH_SET_BUTTON_MESSAGE,
                ),
                self.set_db_path_callback(),
            )
        else:
            DatabaseManager.init_db(CONFIG.db_path)

            accounts = AccountsManager.get_all_accounts()
            if not len(accounts):
                self.push_screen(
                    AddAccountScreen(is_first_account=True),
                    callback=self.show_accounts_screen,
                )
            else:
                self.show_accounts_screen(True)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
