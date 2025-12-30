from __future__ import annotations

from textual.containers import VerticalScroll, Container
from textual.app import ComposeResult

from tuitask.ui.widgets.task_card import TaskCard
from tuitask.ui.widgets.tasks_shared import TaskDisplay

class TasksCardsView(VerticalScroll):
    """Grid view for tasks (Card View)."""
    
    def compose(self) -> ComposeResult:
        yield Container(id="cards-grid")

    def on_mount(self) -> None:
        self.on_resize(None)

    def set_tasks(self, tasks: list[TaskDisplay]) -> None:
        grid = self.query_one("#cards-grid", Container)
        grid.remove_children()
        for t in tasks:
            grid.mount(TaskCard(t))

    def on_resize(self, event) -> None:
        grid = self.query_one("#cards-grid", Container)
        if self.size.width >= 140:
            grid.remove_class("one-col")
            grid.add_class("two-col")
        else:
            grid.remove_class("two-col")
            grid.add_class("one-col")
