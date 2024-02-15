from loguru import logger
from textual import on
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, SelectionList
from textual.widgets.selection_list import Selection

from src.accounting.managers import AccountsManager, BaseMoneyManager
from src.consts import (
    UI_ADD_ACCOUNT_BUTTON_MESSAGE,
    UI_ADD_ACCOUNT_INITIAL_VALUE_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_INPUT_PLACEHOLDER,
    UI_ADD_ACCOUNT_LABEL_MESSAGE,
    UI_ADD_ACCOUNT_LABEL_TITLE,
    UI_ALL_ACCOUNTS_SELECT_TITLE,
    UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE,
    UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE,
    UI_NOT_ACCOUNTS_MESSAGE,
)
from src.ui.screens.warnings import WarningScreenCommon


class AccountsScreen(ModalScreen):
    """
    Экран с выбором виртуального счета.
    """

    def update_selection_list(self):
        accounts_list = AccountsManager.get_formatted_accounts()
        self.query_one(SelectionList).clear_options()
        for account in accounts_list:
            self.query_one(SelectionList).add_option(Selection(*account))

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = UI_ALL_ACCOUNTS_SELECT_TITLE
        self.update_selection_list()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield SelectionList()

    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        try:
            selected_account = self.query_one(SelectionList).selected[0]
        except IndexError as e:
            logger.error(e)
        else:
            self.dismiss(result=selected_account)


class AddAccountScreen(ModalScreen):
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
        _ = AccountsManager.add_account(self.account_name.value, self.account_initial_value.value)
        self.dismiss(result=True)

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
