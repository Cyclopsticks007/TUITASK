from textual.widgets import Static
from textual.containers import Horizontal
from textual.app import ComposeResult

class FooterBar(Static):
    """Global Footer Bar with hints."""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static(" [A] Add Task  [T] Toggle View  [Q] Quit", classes="footer-hints")
            yield Static(" TUITASK V3 ", classes="footer-ver Muted")
