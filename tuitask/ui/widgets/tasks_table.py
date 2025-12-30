from textual.widgets import Static, DataTable, Input, Label
from textual.containers import Vertical, Horizontal, Container
from textual.app import ComposeResult
from textual import on
from rich.text import Text

from tuitask.models.task import Task

class TasksTableView(Container):
    """Table view for tasks."""

    def compose(self) -> ComposeResult:
        # Filter Row
        with Horizontal(id="table-filters"):
            yield Input(placeholder="Status", classes="filter-input", id="f-status")
            yield Input(placeholder="Priority", classes="filter-input", id="f-pri")
            yield Input(placeholder="Title", classes="filter-input", id="f-title")
            yield Input(placeholder="Assignee", classes="filter-input", id="f-assignee")
            yield Input(placeholder="Tags", classes="filter-input", id="f-tags")

        # Table
        yield DataTable(id="tasks-data-table", cursor_type="row")

    def on_mount(self):
        table = self.query_one("#tasks-data-table", DataTable)
        table.add_columns("ID", "Status", "Title", "Assignee", "Priority", "Due", "Phase")

    def set_tasks(self, tasks: list[Task]):
        table = self.query_one("#tasks-data-table", DataTable)
        table.clear()
        
        for t in tasks:
            # Rich Styling
            status_style = "bold white"
            if "Done" in t.status: status_style = "bold green"
            elif "Start" in t.status: status_style = "bold blue"
            
            status_pill = Text(f" {t.status} ", style=f"{status_style} on #1E1E28")
            
            pri_style = "red" if t.priority >= 4 else "white"
            priority = Text(str(t.priority), style=pri_style)
            
            table.add_row(
                str(t.id),
                status_pill,
                t.title,
                t.assignee,
                priority,
                str(t.due_date),
                str(t.phase_id), # TODO: Resolve phase name?
                key=str(t.id)
            )
