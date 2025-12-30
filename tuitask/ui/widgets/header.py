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
            yield Button("Tasks", classes="tab active", id="tab-tasks")
            yield Button("Insights", classes="tab", id="tab-insights")

        with Horizontal(id="header_right"):
            yield Static("LOCAL", classes="header-instance Muted")
            yield Button("+", variant="primary", id="btn-global-create")

    @on(Button.Pressed, "#btn-global-create")
    def on_create_clicked(self):
        self.post_message(self.OpenCreateModal(default_kind="task"))

    class OpenCreateModal(Message):
        def __init__(self, default_kind: str):
            self.default_kind = default_kind
            super().__init__()
