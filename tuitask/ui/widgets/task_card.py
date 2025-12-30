from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Static
from textual.app import ComposeResult
from textual import on

from tuitask.models.task import Task

class TaskCard(Container):
    """Immaculate Task Card."""
    
    def __init__(self, task: Task):
        super().__init__()
        self.task_data = task

    def compose(self) -> ComposeResult:
        t = self.task_data
        
        # Row 1: Status Dot + Title + P value
        with Horizontal(classes="card-top"):
            # yield Static("● ", classes="Accent")
            yield Label(t.title, classes="card-title")
            yield Label(f"P{t.priority}", classes="card-p5")

        # Row 2: Breadcrumb (Project -> Phase) - Mocked for now or need join
        # Just showing ID for now
        with Horizontal(classes="card-mid"):
             yield Label(f"#{t.id} • {t.status}", classes="card-crumb")

        # Row 3: Chips
        with Horizontal(classes="card-bot"):
             yield Label(f"{t.assignee}", classes="chip")
             yield Label(f"Due {t.due_date}", classes="chip")
             
    def on_click(self):
        # Bubble event
        pass
