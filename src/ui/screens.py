from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label

from src.consts import UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE, UI_DB_PATH_SET_BUTTON_MESSAGE


class DbWarningScreen(Screen):
    """
    Экран с предупреждением о необходимости задать путь к файлу с БД.
    """

    def on_button_pressed(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Center(Label(UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE))
        yield Center(
            Button(label=UI_DB_PATH_SET_BUTTON_MESSAGE, variant="success", id="db_set_button")
        )
