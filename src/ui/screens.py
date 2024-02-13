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
    UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE,
    UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE,
    UI_NOT_ACCOUNTS_MESSAGE,
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
        button_label: str = UI_BUTTON_OK_LABEL,
    ) -> None:
        super().__init__(name, id, classes)
        self.message_to_show = message_to_show
        self.button_label = button_label

    def on_button_pressed(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        with Container():
            yield Center(Label(self.message_to_show))
            yield Center(Button(label=self.button_label))


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
        self.dismiss()

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
