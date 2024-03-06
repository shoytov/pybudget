from loguru import logger
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, Select, Tab, Tabs

from src.accounting.managers.categories import CategoriesManager
from src.consts import (
    UI_ADD_TRANSACTION_AMOUNT_INPUT_PLACEHOLDER,
    UI_ADD_TRANSACTION_DESCRIPTION_INPUT_PLACEHOLDER,
    UI_ADD_TRANSACTION_LABEL_MESSAGE,
    UI_BUTTON_OK_LABEL,
    UI_CATEGORY_EXPENSE_LABEL,
    UI_CATEGORY_INCOME_LABEL,
    UI_CATEGORY_TRANSFER_LABEL,
    UI_SELECT_CATEGORY_LIST_PLACEHOLDER,
)
from src.exceptions import EmptyAccountIdentifierError


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
        self.categories_transfer_from = Select(options=[])
        self.categories_transfer_to = Select(options=[])

    def action_close_screen(self) -> None:
        self.dismiss(True)

    def on_mount(self) -> None:
        self.query_one(Tabs).focus()
        self.categories_transfer_from.display = False
        self.categories_transfer_to.display = False
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
            self.categories_transfer_from.display = False
            self.categories_transfer_to.display = False
            self.categories.display = True
        else:
            self.categories_transfer_from.display = True
            self.categories_transfer_to.display = True
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
        yield self.categories_transfer_from
        yield self.categories_transfer_to
        yield Center(self.amount)
        yield Center(self.description)
        yield Center(Button(label=UI_BUTTON_OK_LABEL))
