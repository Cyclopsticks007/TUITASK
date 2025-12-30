from __future__ import annotations

from datetime import date
from typing import Iterable

from textual.containers import Container, Vertical
from textual.app import ComposeResult
from textual.reactive import reactive
from textual import on, work

from tuitask.ui.widgets.header import HeaderBar
from tuitask.ui.widgets.footer import FooterBar
from tuitask.ui.widgets.projects import ProjectsPanel, InsightsPanel
from tuitask.ui.widgets.phases import PhasesPanel, FiltersPanel
from tuitask.ui.widgets.tasks_toolbar import TasksToolbar
from tuitask.ui.widgets.tasks_table import TasksTableView
from tuitask.ui.widgets.tasks_cards import TasksCardsView
from tuitask.ui.widgets.tasks_shared import TaskDisplay
from tuitask.ui.screens.create_modal import CreateModal

from tuitask.viewmodels.tasks_viewmodel import TasksViewModel

class TasksScreen(Container):
    """Bagels-inspired Tasks screen."""

    CSS_PATH = "../theme.tcss"

    BINDINGS = [
        ("a", "open_create('task')", "Add"),
        ("t", "toggle_view", "Toggle View"),
        ("q", "quit", "Quit"),
    ]

    selected_project_id: reactive[int | None] = reactive(None)
    selected_phase_id: reactive[int | None] = reactive(None)
    view_mode: reactive[str] = reactive("table")
    hierarchy_cache: reactive[list] = reactive([])
    tasks_cache: reactive[list] = reactive([])
    table_filters: reactive[dict] = reactive({})
    panel_filters: reactive[dict] = reactive({})

    def compose(self) -> ComposeResult:
        yield HeaderBar(id="HeaderBar")

        with Container(id="BodyGrid"):
            with Vertical():
                yield ProjectsPanel(id="ProjectsPanel")
                yield InsightsPanel(id="InsightsPanel")

            with Vertical():
                yield PhasesPanel(id="PhasesPanel")
                yield FiltersPanel(id="FiltersPanel")

            with Vertical():
                yield TasksToolbar(id="TasksToolbar")
                with Container(id="TasksStack"):
                    yield TasksTableView(id="TasksTableView")
                    yield TasksCardsView(id="TasksCardsView")

        yield FooterBar(id="FooterBar")

    def on_mount(self) -> None:
        self.sync_view_mode()
        self.load_hierarchy()
        self.load_tasks()

    @work(exclusive=True)
    async def load_hierarchy(self) -> None:
        vm = TasksViewModel()
        self.hierarchy_cache = await vm.get_hierarchy()
        self.query_one(ProjectsPanel).set_projects(self.hierarchy_cache)
        self.refresh_phases()
        self.refresh_task_views()

    @work(exclusive=True)
    async def load_tasks(self) -> None:
        vm = TasksViewModel()
        self.tasks_cache = await vm.get_all_tasks()
        self.refresh_task_views()

    def refresh_phases(self) -> None:
        phases_panel = self.query_one(PhasesPanel)
        phases = []
        for project in self.hierarchy_cache:
            if self.selected_project_id is None or project.id == self.selected_project_id:
                phases.extend(project.phases)
        phases_panel.set_phases(phases)

    def refresh_task_views(self) -> None:
        task_items = self.build_task_items()
        table_view = self.query_one(TasksTableView)
        cards_view = self.query_one(TasksCardsView)
        table_view.set_tasks(task_items)
        cards_view.set_tasks(task_items)

    def build_task_items(self) -> list[TaskDisplay]:
        phase_lookup: dict[int, tuple[int | None, str, str]] = {}
        for project in self.hierarchy_cache:
            for phase in project.phases:
                phase_lookup[phase.id] = (project.id, project.name, phase.name)

        items: list[TaskDisplay] = []
        for task in self.tasks_cache:
            project_id = None
            project_name = "Unknown Project"
            phase_name = "Unassigned"
            if task.phase_id in phase_lookup:
                project_id, project_name, phase_name = phase_lookup[task.phase_id]
            items.append(TaskDisplay(task=task, project_name=project_name, phase_name=phase_name, project_id=project_id))

        return self.apply_filters(items)

    def apply_filters(self, items: Iterable[TaskDisplay]) -> list[TaskDisplay]:
        filters = {**self.panel_filters, **self.table_filters}
        status = filters.get("status", "").strip().lower()
        priority = filters.get("priority", "").strip()
        title = filters.get("title", "").strip().lower()
        assignee = filters.get("assignee", "").strip().lower()
        tags = filters.get("tags", "").strip().lower()
        due_window = filters.get("due_window", "")

        filtered: list[TaskDisplay] = []
        today = date.today()

        for item in items:
            task = item.task

            if self.selected_project_id and item.project_id != self.selected_project_id:
                continue
            if self.selected_phase_id and task.phase_id != self.selected_phase_id:
                continue
            if status and status not in task.status.lower():
                continue
            if priority and str(task.priority) != priority:
                continue
            if title and title not in task.title.lower():
                continue
            if assignee and assignee not in task.assignee.lower():
                continue
            if tags and not any(tags in tag.lower() for tag in task.tags):
                continue
            if due_window:
                days_until_due = (task.due_date - today).days
                if due_window == "overdue" and days_until_due >= 0:
                    continue
                if due_window == "next_7" and not (0 <= days_until_due <= 7):
                    continue
                if due_window == "next_30" and not (0 <= days_until_due <= 30):
                    continue
            filtered.append(item)

        return filtered

    def sync_view_mode(self) -> None:
        table = self.query_one("#TasksTableView")
        cards = self.query_one("#TasksCardsView")
        if self.view_mode == "table":
            table.remove_class("-hidden")
            cards.add_class("-hidden")
        else:
            cards.remove_class("-hidden")
            table.add_class("-hidden")
        self.query_one(TasksToolbar).set_mode(self.view_mode)

    def action_toggle_view(self) -> None:
        self.view_mode = "cards" if self.view_mode == "table" else "table"
        self.sync_view_mode()

    def action_open_create(self, kind: str = "task") -> None:
        self.open_create_modal(kind=kind)

    def open_create_modal(self, kind: str = "task") -> None:
        self.app.push_screen(
            CreateModal(
                default_kind=kind,
                hierarchy=self.hierarchy_cache,
                default_project_id=self.selected_project_id,
                default_phase_id=self.selected_phase_id,
            ),
            callback=self.on_item_created,
        )

    def on_item_created(self, result: dict | None = None) -> None:
        if result:
            self.load_hierarchy()
            self.load_tasks()
            self.app.notify(f"Created {result.get('type', 'item')}: {result.get('title', '')}")

    @on(TasksToolbar.ViewModeChanged)
    def on_view_mode(self, event: TasksToolbar.ViewModeChanged) -> None:
        self.view_mode = event.mode
        self.sync_view_mode()

    @on(ProjectsPanel.ProjectSelected)
    def on_project_selected(self, event: ProjectsPanel.ProjectSelected) -> None:
        self.selected_project_id = event.project_id
        self.selected_phase_id = None
        self.refresh_phases()
        self.refresh_task_views()

    @on(PhasesPanel.PhaseSelected)
    def on_phase_selected(self, event: PhasesPanel.PhaseSelected) -> None:
        self.selected_phase_id = event.phase_id
        self.refresh_task_views()

    @on(TasksToolbar.NewTaskRequested)
    def on_task_request(self, event: TasksToolbar.NewTaskRequested) -> None:
        self.open_create_modal(kind="task")

    @on(HeaderBar.OpenCreateModal)
    def on_header_create(self, event: HeaderBar.OpenCreateModal) -> None:
        self.open_create_modal(kind=event.default_kind)

    @on(TasksTableView.FiltersChanged)
    def on_table_filters(self, event: TasksTableView.FiltersChanged) -> None:
        self.table_filters = event.filters
        self.refresh_task_views()

    @on(FiltersPanel.FiltersChanged)
    def on_panel_filters(self, event: FiltersPanel.FiltersChanged) -> None:
        self.panel_filters = event.filters
        self.refresh_task_views()
