from loguru import logger
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, Select, Tab, Tabs

from src.accounting.managers.accounts import AccountsManager
from src.accounting.managers.base import BaseMoneyManager
from src.accounting.managers.categories import CategoriesManager
from src.consts import (
    UI_ADD_TRANSACTION_AMOUNT_INPUT_PLACEHOLDER,
    UI_ADD_TRANSACTION_DESCRIPTION_INPUT_PLACEHOLDER,
    UI_ADD_TRANSACTION_LABEL_MESSAGE,
    UI_BAD_CATEGORY_LABEL_MESSAGE,
    UI_BUTTON_OK_LABEL,
    UI_CATEGORY_EXPENSE_LABEL,
    UI_CATEGORY_INCOME_LABEL,
    UI_CATEGORY_TRANSFER_LABEL,
    UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE,
    UI_SELECT_ACCOUNT_TRANSER_LIST_PLACEHOLDER,
    UI_SELECT_CATEGORY_LIST_PLACEHOLDER,
)
from src.exceptions import EmptyAccountIdentifierError
from src.ui.screens.warnings import WarningScreenCommon


class AddTransactionScreen(ModalScreen):
    BINDINGS = [
        ("escape", "close_screen", ""),
    ]

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        account_id: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        try:
            self.account_id = account_id
        except TypeError as e:
            logger.error(e)
            raise EmptyAccountIdentifierError()
        self.amount = Input(placeholder=UI_ADD_TRANSACTION_AMOUNT_INPUT_PLACEHOLDER)
        self.description = Input(placeholder=UI_ADD_TRANSACTION_DESCRIPTION_INPUT_PLACEHOLDER)
        self.categories = Select(
            prompt=UI_SELECT_CATEGORY_LIST_PLACEHOLDER,
            options=[],
        )
        self.transfer_to_account = Select(
            prompt=UI_SELECT_ACCOUNT_TRANSER_LIST_PLACEHOLDER,
            options=[],
        )

    def on_button_pressed(self) -> None:
        if BaseMoneyManager.validate_amount(self.amount.value) is False:
            self.app.push_screen(
                WarningScreenCommon(message_to_show=UI_INCORRECT_AMOUNT_VALUE_LABEL_MESSAGE)
            )
            return

        category_check = False
        categoty_is_income = False
        tab_label = str(self.query_one(Tabs).active_tab.label)  # type: ignore

        if tab_label == UI_CATEGORY_EXPENSE_LABEL:
            category_check = True
            categoty_is_income = False
        elif tab_label == UI_CATEGORY_INCOME_LABEL:
            category_check = True
            categoty_is_income = True
        else:
            category_check = False

        if category_check is True:
            if not CategoriesManager.validate_category(
                str(self.categories.value), categoty_is_income
            ):
                self.app.push_screen(
                    WarningScreenCommon(message_to_show=UI_BAD_CATEGORY_LABEL_MESSAGE)
                )
                return

    def action_close_screen(self) -> None:
        self.dismiss(True)

    def on_mount(self) -> None:
        self.query_one(Tabs).focus()
        self.transfer_to_account.display = False
        self.categories.display = True

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        if str(event.tab.label) == UI_CATEGORY_EXPENSE_LABEL:
            self.categories.set_options(
                CategoriesManager.get_formatted_all_categories(is_income=False)  # type: ignore
            )
        elif str(event.tab.label) == UI_CATEGORY_INCOME_LABEL:
            self.categories.set_options(
                CategoriesManager.get_formatted_all_categories(is_income=True)  # type: ignore
            )
            self.transfer_to_account.display = False
            self.categories.display = True
        else:
            self.transfer_to_account.set_options(
                AccountsManager.get_formatted_accounts_with_excluded(  # type: ignore
                    (self.account_id,)
                )
            )
            self.transfer_to_account.display = True
            self.categories.display = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Center(Label(UI_ADD_TRANSACTION_LABEL_MESSAGE))
        yield Tabs(
            Tab(UI_CATEGORY_EXPENSE_LABEL),
            Tab(UI_CATEGORY_INCOME_LABEL),
            Tab(UI_CATEGORY_TRANSFER_LABEL),
        )
        yield Center(self.categories)
        yield self.transfer_to_account
        yield Center(self.amount)
        yield Center(self.description)
        yield Center(Button(label=UI_BUTTON_OK_LABEL))
