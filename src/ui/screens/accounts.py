from loguru import logger
from textual import on
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, SelectionList
from textual.widgets.selection_list import Selection

from src.accounting.managers.accounts import AccountsManager
from src.accounting.managers.base import BaseMoneyManager
from src.accounting.managers.transactions import TransactionsManager
from src.core.consts import (
    UI_ACCOUNT_TRANSACTIONS_TITLE,
    UI_ACCOUNTS_SCREEN_LABEL_MESSAGE,
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
from src.exceptions import EmptyAccountIdentifierError
from src.ui.screens.transactions import AddTransactionScreen
from src.ui.screens.warnings import WarningScreenCommon


class AccountScreen(ModalScreen):
    """
    Экран вирутального счета.
    """

    BINDINGS = [("escape", "close_screen", ""), ("a", "add_transaction", "")]

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        account_id: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        try:
            self.account_id = int(account_id)  # type: ignore
        except TypeError as e:
            logger.error(e)
            raise EmptyAccountIdentifierError()

    def action_close_screen(self) -> None:
        self.dismiss(True)

    def action_add_transaction(self) -> None:
        self.app.push_screen(AddTransactionScreen(account_id=self.account_id))  # type: ignore

    def update_selection_list(self):
        transactions_list = TransactionsManager.get_account_formatted_transactions(
            self.account_id  # type: ignore
        )
        self.query_one(SelectionList).clear_options()
        for transaction in transactions_list:
            self.query_one(SelectionList).add_option(Selection(*transaction))

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = UI_ACCOUNT_TRANSACTIONS_TITLE
        self.update_selection_list()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield SelectionList()


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
        yield Center(Label(UI_ACCOUNTS_SCREEN_LABEL_MESSAGE))
        yield SelectionList()

    @on(SelectionList.SelectedChanged)
    def update_selected_view(self) -> None:
        try:
            selected_account = self.query_one(SelectionList).selected[0]
        except IndexError as e:
            logger.error(e)
        else:
            self.dismiss(selected_account)


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

    def on_button_pressed(self) -> None:
        if AccountsManager.validate_account_name(self.account_name.value) is False:
            self.app.push_screen(
                WarningScreenCommon(message_to_show=UI_INCORRECT_ACCOUNT_NAME_LABEL_MESSAGE)
            )
            return
        if BaseMoneyManager.validate_amount(self.account_initial_value.value) is False:
            self.app.push_screen(
                WarningScreenCommon(message_to_show=UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE)
            )
            return
        _ = AccountsManager.add_account(self.account_name.value, self.account_initial_value.value)
        self.dismiss(True)

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
