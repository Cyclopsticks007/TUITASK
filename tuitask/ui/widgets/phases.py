from textual.widgets import Static, ListView, ListItem, Label, Input, RadioSet, RadioButton
from textual.containers import Vertical, Container
from textual.app import ComposeResult
from textual.message import Message
from textual import on

from tuitask.models.phase import Phase

class PhaseItem(ListItem):
    """A single phase item."""
    def __init__(self, phase: Phase):
        super().__init__()
        self.phase = phase

    def compose(self) -> ComposeResult:
        yield Label(f"{self.phase.name}", classes="phase-name")

class PhasesPanel(Container):
    """Column B: Phases List."""
    
    DEFAULT_CSS = """
    PhasesPanel {
    }
    """

    class PhaseSelected(Message):
        def __init__(self, phase_id: int):
            self.phase_id = phase_id
            super().__init__()

    def __init__(self):
        super().__init__(classes="Panel")
        self.border_title = "Phases (f)"

    def compose(self) -> ComposeResult:
        # yield Input(placeholder="Search phases...", id="input-phase-filter")
        yield ListView(id="list-phases")

    def set_phases(self, phases: list[Phase]):
        list_view = self.query_one("#list-phases", ListView)
        list_view.clear()
        for p in phases:
            list_view.append(PhaseItem(p))

    @on(ListView.Selected)
    def on_selection(self, event: ListView.Selected):
        if isinstance(event.item, PhaseItem):
            self.post_message(self.PhaseSelected(event.item.phase.id))

class FiltersPanel(Container):
    """Column B: Task Filters."""
    def __init__(self):
        super().__init__(classes="Panel")
        self.border_title = "Filters"

    def compose(self) -> ComposeResult:
        yield Label("Status", classes="Muted")
        with RadioSet(id="filter-status"):
            yield RadioButton("All", value=True)
            yield RadioButton("Open")
            yield RadioButton("Done")
        
        yield Label("\nAssignee", classes="Muted")
        yield Input(placeholder="Name...", id="filter-assignee")
