from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from src.consts import (
    UI_ADD_ACCOUNT_BUTTON_MESSAGE,
    UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_INPUT_PLACEHOLDER,
    UI_ADD_ACCOUNT_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_LABEL_TITLE,
    UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE,
    UI_DB_PATH_SET_BUTTON_MESSAGE,
    UI_NOT_ACCOUNTS_MESSAGE,
)


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


class AddAccountScreen(Screen):
    """
    Экран для добавления счета.
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        is_first_account: bool = False,
    ) -> None:
        super().__init__(name, id, classes)
        self.is_first_account = is_first_account

    def on_button_pressed(self):
        pass

    def compose(self) -> ComposeResult:
        self.account_name = Input(placeholder=UI_ADD_ACCOUNT_INPUT_PLACEHOLDER)
        self.account_initial_value = Input(placeholder=UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE)

        yield Header()
        yield Footer()

        if self.is_first_account is True:
            yield Center(Label(UI_NOT_ACCOUNTS_MESSAGE))
        yield Center(Label(UI_ADD_ACCOUNT_LABEL_TITLE))
        yield Center(Label(UI_ADD_ACCOUNT_LABEL_MESSAGE))

        yield self.account_name
        yield self.account_initial_value
        yield Center(Button(label=UI_ADD_ACCOUNT_BUTTON_MESSAGE, variant="success"))
