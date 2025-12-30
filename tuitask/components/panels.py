from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Label, Button
from textual.app import ComposeResult

class AccountsPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "Accounts @= 5..."
        with Vertical(classes="account-list"):
            yield Static("Bank    4924.5", classes="account-row highlight")
            yield Static("Card      80.0", classes="account-row")

class InsightsPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "Insights"
        yield Static("Expense of 17 Nov - 23    Expense per day")
        yield Static("1262.5                    180.36", classes="insight-big-num")
        yield Static("//////////////////////////////////////", classes="bar-chart-mock")
        yield Static("● Housing   95% (1200)")
        yield Static("● Food       3% (42)")
        yield Static("● Transport  2% (20)")

class TemplatesPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "Templates"
        with Horizontal():
            yield Button("● Home->Uni\n1", classes="template-btn")
            yield Button("● Monthly Rent\n2", classes="template-btn")
            yield Button("● Netflix Subscription\n3", classes="template-btn")

class RecordsPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "Records"
        yield Label("Date (q)                        Person (w)", classes="record-header-row")
        yield Label("Filter category   Filter amount   Filter label", classes="filter-row")
        yield Static("Category          Amount    Label             Account", classes="table-header")
        yield Static("// 18/11", classes="date-divider")
        yield Static("  ● Salary        + 1200.0  Wage pay          Bank")
        yield Static("  ● Restaurants   - 50.0    Dinner with Sarah Bank")
        yield Static("  × Sarah         + 25.0    -                 -")

class HostingPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "System Status"
        yield Static("Mode: Self-hosted / Raspberry Pi")
        yield Static("Status: Online • 4 active users")
        yield Static("Sync: Async realtime")
        yield Static("Database: SQLite (local cache)")
