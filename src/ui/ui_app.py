from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual_fspicker import SelectDirectory

from src.consts import UI_DB_SET_LABEL_MESSAGE
from src.resources.core import CONFIG
from src.resources.database.manager import DatabaseManager
from src.ui.screens import DbWarningScreen


class BudgetApp(App):
    TITLE = "PyBudget: персональный учет денежных средств"
    BINDINGS = [
        Binding("q", "quit", "Quit", key_display="Q / CTRL+C"),
        Binding("Q", "quit", "Quit"),
    ]

    def db_select_dir_callback(self, path: Path | None):
        DatabaseManager.init_db(path)

    def set_db_path_callback(self) -> None:
        self.push_screen(
            SelectDirectory(title=UI_DB_SET_LABEL_MESSAGE), callback=self.db_select_dir_callback
        )

    def on_ready(self) -> None:
        # если в конфиге отсутствует путь к файлу sqlite
        if not CONFIG.db_path:
            self.push_screen(DbWarningScreen(), self.set_db_path_callback())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
