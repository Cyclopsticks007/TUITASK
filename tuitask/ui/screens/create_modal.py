from __future__ import annotations

from datetime import date

from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button, Input, Select, SegmentedControl
from textual.app import ComposeResult
from textual.reactive import reactive
from textual import on, work

from tuitask.models.task import Task
from tuitask.models.project import Project
from tuitask.viewmodels.tasks_viewmodel import TasksViewModel


class CreateModal(ModalScreen):
    """Modal for creating Projects, Phases, or Tasks."""

    DEFAULT_CSS = """
    CreateModal {
        align: center middle;
    }
    #modal-dialog {
        padding: 2;
        width: 70;
        height: auto;
        background: #202038;
        border: solid #B898F0;
    }
    .modal-title {
        text-align: center;
        text-style: bold;
        color: #B898F0;
        margin-bottom: 1;
    }
    #modal-segmented {
        width: 1fr;
        margin-bottom: 1;
    }
    .modal-actions {
        layout: horizontal;
        align: right middle;
        margin-top: 1;
    }
    Input, Select {
        margin-bottom: 1;
    }
    """

    kind: reactive[str] = reactive("task")

    def __init__(
        self,
        default_kind: str = "task",
        hierarchy: list[Project] | None = None,
        default_project_id: int | None = None,
        default_phase_id: int | None = None,
    ) -> None:
        super().__init__()
        self.kind = default_kind
        self.hierarchy = hierarchy or []
        self.default_project_id = default_project_id
        self.default_phase_id = default_phase_id

    def compose(self) -> ComposeResult:
        with Container(id="modal-dialog"):
            yield Label("Create New Item", classes="modal-title")
            yield SegmentedControl(
                ("Project", "Phase", "Task"),
                id="modal-segmented",
                value=self.kind.capitalize(),
            )

            with Vertical(id="form-project"):
                yield Input(placeholder="Project name", id="project-name")
                yield Input(placeholder="Description", id="project-desc")

            with Vertical(id="form-phase"):
                yield Select(self.project_options(), id="phase-project")
                yield Input(placeholder="Phase name", id="phase-name")
                yield Input(placeholder="Description", id="phase-desc")

            with Vertical(id="form-task"):
                yield Select(self.project_options(), id="task-project")
                yield Select(self.phase_options(self.default_project_id), id="task-phase")
                yield Input(placeholder="Task title", id="task-title")
                yield Input(placeholder="Assignee", id="task-assignee")
                yield Input(placeholder="Priority (1-5)", id="task-priority")
                yield Input(placeholder="Due date (YYYY-MM-DD)", id="task-due")
                yield Input(placeholder="Tags (comma)", id="task-tags")
                yield Input(placeholder="Status", id="task-status")

            with Horizontal(classes="modal-actions"):
                yield Button("Cancel", variant="default", id="btn-cancel")
                yield Button("Create", variant="primary", id="btn-create")

    def on_mount(self) -> None:
        self.sync_forms()
        self.apply_defaults()

    def sync_forms(self) -> None:
        self.query_one("#form-project").display = self.kind == "project"
        self.query_one("#form-phase").display = self.kind == "phase"
        self.query_one("#form-task").display = self.kind == "task"

    def apply_defaults(self) -> None:
        if self.default_project_id is not None:
            self.query_one("#phase-project", Select).value = self.default_project_id
            self.query_one("#task-project", Select).value = self.default_project_id
            self.update_phase_select(self.default_project_id)
        if self.default_phase_id is not None:
            self.query_one("#task-phase", Select).value = self.default_phase_id

    def project_options(self) -> list[tuple[str, int | str]]:
        options = [("Select project", "")]
        options.extend((project.name, project.id) for project in self.hierarchy if project.id is not None)
        return options

    def phase_options(self, project_id: int | None) -> list[tuple[str, int | str]]:
        options = [("Select phase", "")]
        if project_id is None:
            return options
        for project in self.hierarchy:
            if project.id == project_id:
                options.extend((phase.name, phase.id) for phase in project.phases if phase.id is not None)
        return options

    def update_phase_select(self, project_id: int | None) -> None:
        phase_select = self.query_one("#task-phase", Select)
        phase_select.set_options(self.phase_options(project_id))
        if self.default_phase_id is not None:
            phase_select.value = self.default_phase_id

    @on(SegmentedControl.Changed, "#modal-segmented")
    def on_segmented_changed(self, event: SegmentedControl.Changed) -> None:
        self.kind = event.value.lower()
        self.sync_forms()

    @on(Select.Changed, "#task-project")
    def on_task_project_changed(self, event: Select.Changed) -> None:
        self.update_phase_select(event.value or None)

    @on(Button.Pressed, "#btn-cancel")
    def on_cancel(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#btn-create")
    def on_create(self) -> None:
        self.create_item()

    @work(exclusive=True)
    async def create_item(self) -> None:
        vm = TasksViewModel()
        if self.kind == "project":
            name = self.query_one("#project-name", Input).value.strip()
            description = self.query_one("#project-desc", Input).value.strip()
            if name:
                await vm.add_project(name=name, description=description)
                self.dismiss(result={"type": "project", "title": name})
            else:
                self.dismiss()
            return

        if self.kind == "phase":
            project_id = self.query_one("#phase-project", Select).value
            name = self.query_one("#phase-name", Input).value.strip()
            if project_id and name:
                await vm.add_phase(project_id=int(project_id), name=name)
                self.dismiss(result={"type": "phase", "title": name})
            else:
                self.dismiss()
            return

        title = self.query_one("#task-title", Input).value.strip()
        assignee = self.query_one("#task-assignee", Input).value.strip() or "Unassigned"
        priority_value = self.query_one("#task-priority", Input).value.strip()
        priority = int(priority_value) if priority_value.isdigit() else 3
        due_value = self.query_one("#task-due", Input).value.strip()
        if due_value:
            try:
                due_date = date.fromisoformat(due_value)
            except ValueError:
                due_date = date.today()
        else:
            due_date = date.today()
        tags = self.query_one("#task-tags", Input).value.strip()
        status = self.query_one("#task-status", Input).value.strip() or "Assigned"
        phase_id = self.query_one("#task-phase", Select).value

        if not title:
            self.dismiss()
            return

        task = Task(
            title=title,
            assignee=assignee,
            priority=priority,
            due_date=due_date,
            tags_str=tags,
            status=status,
            phase_id=int(phase_id) if phase_id else None,
        )
        await vm.add_task(task)
        self.dismiss(result={"type": "task", "title": title})
