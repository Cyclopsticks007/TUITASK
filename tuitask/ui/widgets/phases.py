from textual.widgets import ListView, ListItem, Label, Input, RadioSet, RadioButton, Select
from textual.containers import Container
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
        self.phases: list[Phase] = []

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search phases...", id="input-phase-filter")
        yield ListView(id="list-phases")

    def set_phases(self, phases: list[Phase]):
        self.phases = phases
        self.refresh_list(phases)

    def refresh_list(self, phases: list[Phase]) -> None:
        list_view = self.query_one("#list-phases", ListView)
        list_view.clear()
        for p in phases:
            list_view.append(PhaseItem(p))

    @on(ListView.Selected)
    def on_selection(self, event: ListView.Selected):
        if isinstance(event.item, PhaseItem):
            self.post_message(self.PhaseSelected(event.item.phase.id))

    @on(Input.Changed, "#input-phase-filter")
    def on_filter_changed(self, event: Input.Changed) -> None:
        query = event.value.strip().lower()
        phases = self.phases
        if query:
            phases = [phase for phase in self.phases if query in phase.name.lower()]
        self.refresh_list(phases)

class FiltersPanel(Container):
    """Column B: Task Filters."""
    def __init__(self):
        super().__init__(classes="Panel")
        self.border_title = "Filters"

    class FiltersChanged(Message):
        def __init__(self, filters: dict[str, str]):
            self.filters = filters
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Status", classes="Muted")
        with RadioSet(id="filter-status"):
            yield RadioButton("All", value=True)
            yield RadioButton("Open")
            yield RadioButton("Done")
            yield RadioButton("Blocked")
        
        yield Label("Assignee", classes="Muted")
        yield Input(placeholder="Name...", id="filter-assignee")

        yield Label("Tags", classes="Muted")
        yield Input(placeholder="Design, infra...", id="filter-tags")

        yield Label("Due Window", classes="Muted")
        yield Select(
            (
                ("Any", ""),
                ("Overdue", "overdue"),
                ("Next 7 days", "next_7"),
                ("Next 30 days", "next_30"),
            ),
            id="filter-due",
            value="",
        )

    def on_mount(self) -> None:
        self.emit_filters()

    def emit_filters(self) -> None:
        status = self.query_one("#filter-status", RadioSet).pressed
        status_label = ""
        if status:
            status_label = status.label.plain
            if status_label.lower() == "all":
                status_label = ""
        filters = {
            "status": status_label,
            "assignee": self.query_one("#filter-assignee", Input).value,
            "tags": self.query_one("#filter-tags", Input).value,
            "due_window": self.query_one("#filter-due", Select).value or "",
        }
        self.post_message(self.FiltersChanged(filters))

    @on(RadioSet.Changed)
    def on_status_change(self, event: RadioSet.Changed) -> None:
        self.emit_filters()

    @on(Input.Changed, "#filter-assignee")
    @on(Input.Changed, "#filter-tags")
    @on(Select.Changed, "#filter-due")
    def on_filters_changed(self, event) -> None:
        self.emit_filters()
