from textual.containers import Container, Vertical
from textual.app import ComposeResult
from textual import on, work

from tuitask.ui.widgets.header import HeaderBar
from tuitask.ui.widgets.footer import FooterBar
from tuitask.ui.widgets.projects import ProjectsPanel, InsightsPanel
from tuitask.ui.widgets.phases import PhasesPanel, FiltersPanel
from tuitask.ui.widgets.tasks_toolbar import TasksToolbar
from tuitask.ui.widgets.tasks_table import TasksTableView
from tuitask.ui.widgets.tasks_cards import TasksCardsView

from tuitask.viewmodels.tasks_viewmodel import TasksViewModel

class TasksView(Container):
    """V3 Tasks View."""
    
    CSS_PATH = "../theme.tcss"

    def compose(self) -> ComposeResult:
        yield HeaderBar(id="HeaderBar")
        
        with Container(id="BodyGrid"):
            # Column A
            with Vertical():
                yield ProjectsPanel()
                yield InsightsPanel()
            
            # Column B
            with Vertical():
                yield PhasesPanel()
                yield FiltersPanel()
            
            # Column C
            with Vertical():
                yield TasksToolbar()
                with Container(id="TasksStack"):
                    yield TasksTableView(id="view-table")
                    yield TasksCardsView(id="view-cards")

        yield FooterBar(id="FooterBar")

    def on_mount(self):
        # Initial State: Show table, hide cards
        self.query_one("#view-cards").display = False
        
        # Load Data
        self.load_data()

    @work
    async def load_data(self):
        vm = TasksViewModel()
        
        # Load Projects
        projects = await vm.get_hierarchy() 
        # Note: get_hierarchy returns Projects populated with Phases/Tasks
        self.query_one(ProjectsPanel).set_projects(projects)
        
        # Load ALL tasks initially (or filter?)
        all_tasks = await vm.get_all_tasks()
        self.update_task_views(all_tasks)

    def update_task_views(self, tasks):
        self.query_one(TasksTableView).set_tasks(tasks)
        self.query_one(TasksCardsView).set_tasks(tasks)

    @on(TasksToolbar.ViewModeChanged)
    def on_view_mode(self, event: TasksToolbar.ViewModeChanged):
        table = self.query_one("#view-table")
        cards = self.query_one("#view-cards")
        
        if event.mode == "table":
            table.display = True
            cards.display = False
        else:
            table.display = False
            cards.display = True

    @on(ProjectsPanel.ProjectSelected)
    def on_project_selected(self, event: ProjectsPanel.ProjectSelected):
        # Logic to filter phases and tasks by project
        # For prototype, re-load ALL tasks or filter in memory
        pass

