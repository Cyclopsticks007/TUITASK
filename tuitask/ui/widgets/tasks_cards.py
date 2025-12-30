from textual.containers import VerticalScroll, Container
from textual.app import ComposeResult
from textual.widget import Widget
from textual import on

from tuitask.ui.widgets.task_card import TaskCard
from tuitask.models.task import Task

class TasksCardsView(VerticalScroll):
    """Grid view for tasks (Card View)."""
    
    def compose(self) -> ComposeResult:
        yield Container(id="cards-grid")

    def set_tasks(self, tasks: list[Task]):
        grid = self.query_one("#cards-grid", Container)
        grid.remove_children()
        for t in tasks:
            grid.mount(TaskCard(t))

    def on_resize(self, event):
        # Responsive 2-col logic
        grid = self.query_one("#cards-grid", Container)
        if self.size.width > 120: 
            grid.add_class("two-col")
        else:
            grid.remove_class("two-col")
