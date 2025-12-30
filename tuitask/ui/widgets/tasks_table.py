from __future__ import annotations

from datetime import date

from textual.widgets import DataTable, Input
from textual.containers import Horizontal, Container
from textual.app import ComposeResult
from textual import on
from textual.message import Message
from rich.text import Text

from tuitask.ui.widgets.tasks_shared import TaskDisplay

class TasksTableView(Container):
    """Table view for tasks."""

    class FiltersChanged(Message):
        def __init__(self, filters: dict[str, str]):
            self.filters = filters
            super().__init__()

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
        table.add_columns("Due", "Pri", "Task", "Status", "Assignee", "Tags", "Phase")

    @on(Input.Changed)
    def on_filter_change(self, event: Input.Changed) -> None:
        filters = {
            "status": self.query_one("#f-status", Input).value,
            "priority": self.query_one("#f-pri", Input).value,
            "title": self.query_one("#f-title", Input).value,
            "assignee": self.query_one("#f-assignee", Input).value,
            "tags": self.query_one("#f-tags", Input).value,
        }
        self.post_message(self.FiltersChanged(filters))

    def set_tasks(self, tasks: list[TaskDisplay]) -> None:
        table = self.query_one("#tasks-data-table", DataTable)
        table.clear()
        if not tasks:
            table.add_row(Text("No tasks match the filters.", style="dim"), "", "", "", "", "", "")
            return

        sorted_tasks = sorted(tasks, key=lambda item: (item.phase_name, item.task.due_date))
        current_group = None
        today = date.today()

        for item in sorted_tasks:
            task = item.task
            if item.phase_name != current_group:
                current_group = item.phase_name
                table.add_row(
                    "",
                    "",
                    Text(f"// {current_group}", style="dim"),
                    "",
                    "",
                    "",
                    "",
                    key=f"group:{current_group}",
                )

            status_lower = task.status.lower()
            status_color = "green"
            if "start" in status_lower:
                status_color = "blue"
            elif "blocked" in status_lower or "overdue" in status_lower:
                status_color = "red"
            elif "need" in status_lower:
                status_color = "magenta"
            dot = Text("● ", style=status_color)
            title = Text.assemble(dot, (task.title, "bold"))

            due_style = "bold red" if task.due_date < today else "white"
            due_text = Text(task.due_date.isoformat(), style=due_style)

            priority = Text(str(task.priority), style="red" if task.priority >= 4 else "white")
            status_text = Text(f"{task.status}", style="bold")

            tags = list(task.tags)
            tag_text = Text(", ".join(tag for tag in tags if tag))
            if task.requires_signoff:
                tag_text.append("  SIGNOFF", style="black on #B898F0")

            table.add_row(
                due_text,
                priority,
                title,
                status_text,
                task.assignee,
                tag_text,
                item.phase_name,
                key=str(task.id),
            )
