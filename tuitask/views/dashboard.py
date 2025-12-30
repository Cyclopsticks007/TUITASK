from textual.containers import Container
from textual.app import ComposeResult
from tuitask.components.panels import AccountsPanel, InsightsPanel, TemplatesPanel, RecordsPanel, HostingPanel
from tuitask.components.calendar import CalendarPanel

class DashboardView(Container):
    def compose(self) -> ComposeResult:
        with Container(id="outer_frame"):
            # Main Grid
            with Container(id="main_grid"):
                # Left Region (A+B)
                with Container(id="left_region"):
                     yield AccountsPanel(id="accounts_panel", classes="card")
                     yield InsightsPanel(id="insights_panel", classes="card")
                
                # Center Region (C)
                with Container(id="calendar_region"):
                     yield CalendarPanel(id="calendar_panel")
                     yield HostingPanel(id="hosting_panel", classes="card")

                # Right Region (D+E+F)
                with Container(id="right_region"):
                     yield TemplatesPanel(id="templates_panel", classes="card")
                     yield RecordsPanel(id="records_panel", classes="card")
