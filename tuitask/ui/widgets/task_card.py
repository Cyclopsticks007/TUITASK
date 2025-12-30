from __future__ import annotations

from datetime import date

from textual.containers import Container, Horizontal
from textual.widgets import Label
from textual.app import ComposeResult

from tuitask.ui.widgets.tasks_shared import TaskDisplay

class TaskCard(Container):
    """Immaculate Task Card."""
    
    def __init__(self, task: TaskDisplay):
        super().__init__()
        self.task_data = task

    def compose(self) -> ComposeResult:
        item = self.task_data
        t = item.task
        today = date.today()
        
        # Row 1: Status Dot + Title + P value
        with Horizontal(classes="card-top"):
            yield Label("●", classes=f"status-dot {self.status_class(t.status)}")
            yield Label(t.title, classes="card-title")
            yield Label(f"P{t.priority}", classes="card-priority")

        # Row 2: Breadcrumb
        with Horizontal(classes="card-mid"):
            yield Label(f"{item.project_name} → {item.phase_name}", classes="card-crumb")

        # Row 3: Chips
        with Horizontal(classes="card-tags"):
            for tag in t.tags:
                if tag:
                    yield Label(tag.strip(), classes="chip")
            if t.requires_signoff:
                yield Label("SIGNOFF", classes="chip signoff")

        # Row 4: Assignee + Due
        with Horizontal(classes="card-bot"):
            yield Label(t.assignee, classes="chip")
            due_class = "chip overdue" if t.due_date < today else "chip"
            yield Label(f"Due {t.due_date.isoformat()}", classes=due_class)
            yield Label(t.status, classes="chip muted")

    @staticmethod
    def status_class(status: str) -> str:
        status_lower = status.lower()
        if "start" in status_lower:
            return "status-started"
        if "done" in status_lower or "complete" in status_lower:
            return "status-done"
        if "block" in status_lower:
            return "status-blocked"
        if "need" in status_lower:
            return "status-signoff"
        return "status-open"
