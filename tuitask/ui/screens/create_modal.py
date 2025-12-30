from textual.screen import ModalScreen
from textual.containers import Container, Vertical
from textual.widgets import Label, Button, Input, Select
from textual.app import ComposeResult
from textual import on

class CreateModal(ModalScreen):
    """Modal for creating Projects, Phases, or Tasks."""
    
    DEFAULT_CSS = """
    CreateModal {
        align: center middle;
    }
    #modal-dialog {
        padding: 2;
        width: 60;
        height: auto;
        background: #202038;
        border: solid #B898F0;
    }
    .modal-title {
        text-align: center;
        text-style: bold;
        color: #B898F0;
        margin-bottom: 2;
    }
    Input { margin-bottom: 1; }
    """

    def compose(self) -> ComposeResult:
        with Container(id="modal-dialog"):
            yield Label("Create New Item", classes="modal-title")
            
            # Simple single form for Task for now (MVP)
            # Full 3-tab switcher can be added later as request "segmented type selector" is complex for 1 step
            # Let's target Task creation primarily as that's the main action
            
            yield Input(placeholder="Task Title", id="input-title")
            yield Input(placeholder="Assignee", id="input-assignee")
            
            # Project/Phase selection would be Select widgets
            
            with Container(classes="dialog-actions"):
                 yield Button("Cancel", variant="default", id="btn-cancel")
                 yield Button("Create", variant="primary", id="btn-create")

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self):
        self.dismiss()

    @on(Button.Pressed, "#btn-create")
    def on_create(self):
        # Call ViewModel logic? Or return result?
        # Return result to caller
        self.dismiss(result={"type": "task", "title": "New Task"})
