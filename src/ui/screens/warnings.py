from textual.app import ComposeResult
from textual.containers import Center, Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from src.core.consts import UI_BUTTON_OK_LABEL


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
