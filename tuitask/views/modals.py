from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Label, Button, Input, Select
from textual import on, work
from tuitask.models.project import Project, ProjectLocation
from tuitask.models.phase import Phase
from tuitask.models.task import Task
from tuitask.db.engine import get_session
from tuitask.db.crud import projects as project_crud
from tuitask.db.crud import phases as phase_crud
from tuitask.db.crud import tasks as task_crud
from datetime import date, timedelta

class TaskCreationModal(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label("Create New Task", classes="modal-title")
            yield Input(placeholder="Task Title", id="task_title")
            yield Input(placeholder="Assignee", id="task_assignee")
            yield Input(placeholder="Priority (1-5)", id="task_priority")
            # MVP: Phase selection is hard without a combobox populated from async
            # For now, default to first available or unassigned
            
            with Horizontal():
                yield Button("Save", variant="primary", id="save_btn")
                yield Button("Cancel", id="cancel_btn")

    @on(Button.Pressed, "#cancel_btn")
    def cancel(self):
        self.dismiss()

    @on(Button.Pressed, "#save_btn")
    async def save(self):
        title = self.query_one("#task_title", Input).value
        
        if not title:
             self.app.notify("Title required", severity="error")
             return

        # Simple creation (unassigned for now)
        task = Task(title=title, phase_id=None) 
        
        async for session in get_session():
             await task_crud.create_task(session, task)
             
        self.app.notify(f"Task '{title}' created!")
        self.dismiss(True)

class ProjectCreateModal(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label("Create New Project", classes="modal-title")
            yield Input(placeholder="Project Name", id="proj_name")
            yield Input(placeholder="Timezone (e.g. UTC, EST)", id="proj_tz", value="UTC")
            yield Input(placeholder="Description", id="proj_desc")
            yield Label("Location:")
            yield Select.from_values(["local", "network"], id="proj_loc") 
            
            with Horizontal():
                yield Button("Save", variant="primary", id="save_btn")
                yield Button("Cancel", id="cancel_btn")

    @on(Button.Pressed, "#cancel_btn")
    def cancel(self):
        self.dismiss()

    @on(Button.Pressed, "#save_btn")
    async def save(self):
        name = self.query_one("#proj_name", Input).value
        tz = self.query_one("#proj_tz", Input).value
        desc = self.query_one("#proj_desc", Input).value
        
        loc_val = self.query_one("#proj_loc", Select).value
        if loc_val == Select.BLANK:
             loc = ProjectLocation.LOCAL
        else:
             loc = ProjectLocation(loc_val)

        if not name:
            self.app.notify("Name required", severity="error")
            return

        proj = Project(name=name, timezone=tz, description=desc, location=loc)
        
        async for session in get_session():
            await project_crud.create_project(session, proj)
        
        self.app.notify(f"Project '{name}' created!")
        self.dismiss(True)


class PhaseCreateModal(ModalScreen):
    def __init__(self, project_id: int):
        super().__init__()
        self.project_id = project_id

    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label("Create New Phase", classes="modal-title")
            yield Input(placeholder="Phase Name", id="phase_name")
            yield Input(placeholder="Description", id="phase_desc")
            yield Input(placeholder="Order (1, 2...)", id="phase_order", type="integer")
            
            with Horizontal():
                yield Button("Save", variant="primary", id="save_btn")
                yield Button("Cancel", id="cancel_btn")

    @on(Button.Pressed, "#cancel_btn")
    def cancel(self):
        self.dismiss()

    @on(Button.Pressed, "#save_btn")
    async def save(self):
        name = self.query_one("#phase_name", Input).value
        desc = self.query_one("#phase_desc", Input).value
        order_val = self.query_one("#phase_order", Input).value
        
        try:
             order = int(order_val)
        except:
             order = 0

        if not name:
             self.app.notify("Name required", severity="error")
             return

        phase = Phase(name=name, description=desc, order=order, project_id=self.project_id)
        
        async for session in get_session():
             await phase_crud.create_phase(session, phase)
             
        self.app.notify(f"Phase '{name}' created!")
        self.dismiss(True)
