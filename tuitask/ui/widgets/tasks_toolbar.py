from textual.widgets import Static, Button
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.message import Message
from textual import on

class TasksToolbar(Static):
    """Toolbar for Tasks Column (View Toggle + Actions)."""

    class ViewModeChanged(Message):
        def __init__(self, mode: str):
            self.mode = mode
            super().__init__()

    class NewTaskRequested(Message):
        pass

    def compose(self) -> ComposeResult:
        with Horizontal(id="toolbar-left"):
            # Manual Segmented Control
            with Horizontal(id="view-toggle"):
                yield Button("Table", id="mode-table", classes="view-btn active")
                yield Button("Cards", id="mode-cards", classes="view-btn")

        with Horizontal(id="toolbar-right"):
            yield Button("+ Add Task", variant="primary", id="btn-add-task")

    @on(Button.Pressed, "#btn-add-task")
    def on_add(self):
        self.post_message(self.NewTaskRequested())

    @on(Button.Pressed, ".view-btn")
    def on_view_change(self, event: Button.Pressed):
        selected_btn = event.button
        
        # Toggle classes
        self.query(".view-btn").remove_class("active")
        selected_btn.add_class("active")
        
        mode = "table"
        if selected_btn.id == "mode-cards":
            mode = "cards"
            
        self.post_message(self.ViewModeChanged(mode))
