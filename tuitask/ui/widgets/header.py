from textual.widgets import Static, Button
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual import on
from textual.message import Message

class HeaderBar(Static):
    """Global Header Bar for Tasks Screen."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="header_left"):
            yield Static("TUITASK", classes="header-brand Accent")
            yield Button("Projects", classes="tab active", id="tab-projects")
            # yield Button("Timelines", classes="tab", id="tab-timelines")

        with Horizontal(id="header_right"):
            yield Button("+ New", variant="primary", id="btn-global-create")

    @on(Button.Pressed, "#btn-global-create")
    def on_create_clicked(self):
        self.post_message(self.OpenCreateModal())

    class OpenCreateModal(Message):
        pass
