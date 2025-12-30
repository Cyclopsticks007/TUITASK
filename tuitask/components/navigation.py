from textual.containers import Container, Horizontal
from textual.widgets import Label, Button
from textual.app import ComposeResult

class TopNav(Container):
    def compose(self) -> ComposeResult:
        with Horizontal(id="header_nav"): # Matches CSS spec #header_nav
            # Left: Brand
            yield Label(" ↪ Bagels 0.4.0", id="nav_left")
            
            # Center: Tabs
            with Container(id="nav_center"):
                yield Button("Home", classes="tab active", id="tab-home")
                yield Button("Tasks", classes="tab", id="tab-tasks")
                yield Button("Manager", classes="tab", id="tab-manager")
            
            # Right: Context
            with Container(id="nav_right"):
                 yield Button("Login", variant="primary", id="btn-login", classes="login-btn")
