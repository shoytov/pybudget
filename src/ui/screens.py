from textual.app import ComposeResult
from textual.containers import Center, Container
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Header, Input, Label

from src.accounting.managers import AccountsManager, BaseMoneyManager
from src.consts import (
    UI_ADD_ACCOUNT_BUTTON_MESSAGE,
    UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_INPUT_PLACEHOLDER,
    UI_ADD_ACCOUNT_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_LABEL_TITLE,
    UI_BUTTON_OK_LABEL,
    UI_DB_PATH_NOT_DEFINED_WARNING_MESSAGE,
    UI_DB_PATH_SET_BUTTON_MESSAGE,
    UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE,
    UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE,
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


class WarningScreenCommon(ModalScreen):
    """
    Экран для вывода информационных сообщений.
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        message_to_show: str = "",
    ) -> None:
        super().__init__(name, id, classes)
        self.message_to_show = message_to_show

    def on_button_pressed(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        with Container():
            yield Center(Label(self.message_to_show))
            yield Center(Button(label=UI_BUTTON_OK_LABEL))


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
        if AccountsManager.validate_account_name(self.account_name.value) is False:
            self.app.push_screen(
                WarningScreenCommon(message_to_show=UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE)
            )
        if BaseMoneyManager.validate_amount(self.account_initial_value.value) is False:
            self.app.push_screen(
                WarningScreenCommon(message_to_show=UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE)
            )
        AccountsManager.add_account(self.account_name.value, self.account_initial_value.value)

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
