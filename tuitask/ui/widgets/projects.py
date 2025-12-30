from textual.widgets import ListView, ListItem, Label, Input
from textual.containers import Vertical, Container
from textual.app import ComposeResult
from textual.message import Message
from textual import on

from tuitask.models.project import Project

class ProjectItem(ListItem):
    """A single project item in the list."""
    def __init__(self, project: Project):
        super().__init__()
        self.project = project

    def compose(self) -> ComposeResult:
        yield Label(f"{self.project.name}", classes="project-name")
        # yield Label(f"{self.project.progress}%", classes="project-progress Muted")

class ProjectsPanel(Container):
    """Column A: Projects List."""
    
    DEFAULT_CSS = """
    ProjectsPanel {
        /* Styling handled by .Panel class in theme.tcss */
    }
    """

    class ProjectSelected(Message):
        def __init__(self, project_id: int):
            self.project_id = project_id
            super().__init__()

    def __init__(self):
        super().__init__(classes="Panel")
        self.border_title = "Projects (p)"
        self.projects: list[Project] = []
        self.filtered_projects: list[Project] = []

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Filter projects...", id="input-project-filter")
        yield ListView(id="list-projects")

    def set_projects(self, projects: list[Project]):
        self.projects = projects
        self.filtered_projects = projects
        self.refresh_list()

    def refresh_list(self) -> None:
        list_view = self.query_one("#list-projects", ListView)
        list_view.clear()
        for p in self.filtered_projects:
            list_view.append(ProjectItem(p))

    @on(Input.Changed, "#input-project-filter")
    def on_filter_changed(self, event: Input.Changed) -> None:
        query = event.value.strip().lower()
        if not query:
            self.filtered_projects = self.projects
        else:
            self.filtered_projects = [p for p in self.projects if query in p.name.lower()]
        self.refresh_list()

    @on(ListView.Selected)
    def on_selection(self, event: ListView.Selected):
        if isinstance(event.item, ProjectItem):
            self.post_message(self.ProjectSelected(event.item.project.id))

class InsightsPanel(Container):
    """Column A: Insights (Bottom)."""
    def __init__(self):
        super().__init__(classes="Panel")
        self.border_title = "Insights"

    def compose(self) -> ComposeResult:
        with Vertical(classes="insights-content"):
            yield Label("Velocity:  [bold green]85%[/]", classes="insight-row")
            yield Label("Pending:   [bold white]12[/]", classes="insight-row")
            yield Label("Overdue:   [bold red]3[/]", classes="insight-row")
            yield Label("Next Rel:  [bold blue]v3.1[/]", classes="insight-row")
