from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Label, Static, Button, DataTable, ContentSwitcher
from textual.app import ComposeResult
from textual import on, work
from rich.text import Text

from tuitask.models.task import Task
from tuitask.viewmodels.tasks_viewmodel import TasksViewModel

class TaskTableView(Container):
    def compose(self) -> ComposeResult:
        # DataTable for tabular view
        yield DataTable(id="tasks-data-table", cursor_type="row")

    def on_mount(self):
        table = self.query_one("#tasks-data-table", DataTable)
        table.add_columns("ID", "Status", "Title", "Assignee", "Priority", "Due")

class TaskCard(Container):
    """A 'Tasker' style card with rich metadata."""
    def __init__(self, task: Task):
        super().__init__(classes="task-list-card")
        self.task_data = task

    def compose(self) -> ComposeResult:
        t = self.task_data
        
        # Determine status color for icon
        status_class = f"status-icon-{t.status.lower().replace(' ', '-')}"
        
        with Container(classes="card-row-header"):
            yield Static("●", classes=f"card-status-icon {status_class}")
            yield Label(t.title, classes="card-title")
            # yield Button("⋮", classes="card-menu-btn") # Placeholder for menu

        with Container(classes="card-row-body"):
            # Tags as pills
            if t.tags_str:
                for tag in t.tags_str.split(","):
                    yield Label(tag.strip(), classes="card-tag")
            else:
                yield Label("No tags", classes="card-tag-empty")

        with Container(classes="card-row-footer"):
            # Avatar (Initials)
            initials = t.assignee[:2].upper() if t.assignee else "UN"
            yield Label(initials, classes="avatar-circle")
            
            # Due Date
            yield Label(str(t.due_date), classes="card-due-date")
        
    def on_click(self) -> None:
        self.app.post_message(self.Selected(self.task_data))

    class Selected:
        def __init__(self, task: Task):
            self.task = task

class TaskCardListView(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Container(id="card-list-container")

class TaskBrowserPanel(Container):
    def compose(self) -> ComposeResult:
        # Custom Header
        with Horizontal(id="browser-header"):
             yield Label("My Tasks", classes="browser-title")
             with Horizontal(id="view-switcher-group"):
                 yield Button("List", id="btn-view-table", variant="primary", classes="view-btn left")
                 yield Button("Board", id="btn-view-cards", variant="default", classes="view-btn right")

        with ContentSwitcher(initial="view-table", id="browser-switcher"):
            yield TaskTableView(id="view-table")
            yield TaskCardListView(id="view-cards")

    @on(Button.Pressed, "#btn-view-table")
    def show_table(self):
        self.query_one("#browser-switcher", ContentSwitcher).current = "view-table"
        self.query_one("#btn-view-table").variant = "primary"
        self.query_one("#btn-view-cards").variant = "default"

    @on(Button.Pressed, "#btn-view-cards")
    def show_cards(self):
        self.query_one("#browser-switcher", ContentSwitcher).current = "view-cards"
        self.query_one("#btn-view-table").variant = "default"
        self.query_one("#btn-view-cards").variant = "primary"

class ItemDetailPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "Details"
        with VerticalScroll(id="details-scroll"):
             yield Label("Select a task to view details.", id="detail-header", classes="detail-header")
             yield Container(id="detail-content")

    def render_task(self, task: Task):
        self.border_title = f"Task: {task.title}"
        header = self.query_one("#detail-header", Label)
        header.update(f"{task.title}")
        
        content = self.query_one("#detail-content", Container)
        content.remove_children()
        
        content.mount(
             Label(f"ID: {task.id}", classes="detail-row"),
             Label(f"Status: {task.status}", classes="detail-row"),
             Label(f"Assignee: {task.assignee}", classes="detail-row"),
             Label(f"Priority: {task.priority}", classes="detail-row"),
             Label(f"Start: {task.start_date}", classes="detail-row"),
             Label(f"Due: {task.due_date}", classes="detail-row"),
             Static(f"\nTags: {task.tags_str}", classes="detail-desc"),
             Static(f"\nLinks: {task.links_str}", classes="detail-desc")
        )

class TasksView(Container):
    def compose(self) -> ComposeResult:
        # Actions Bar
        with Horizontal(id="tasks-actions-bar", classes="actions-bar"):
             yield Button("New Project", id="btn-new-proj", variant="primary", classes="action-btn")
             yield Button("New Phase", id="btn-new-phase", variant="default", classes="action-btn")

        with Container(id="tasks-split-view"):
            with Container(id="task-list-container"):
                yield TaskBrowserPanel(id="task-browser-panel")
            
            with Container(id="task-details-container"):
                yield ItemDetailPanel(id="item-detail-panel", classes="card")
        
    def on_mount(self) -> None:
        self.load_tasks()

    def get_status_style(self, status: str) -> str:
        s = status.lower()
        if "start" in s: return "blue"
        if "sign-off" in s: return "red"
        if "assign" in s: return "yellow"
        if "done" in s or "complete" in s: return "green"
        return "white"

    @work(exclusive=True)
    async def load_tasks(self) -> None:
        vm = TasksViewModel()
        tasks = await vm.get_all_tasks()
        
        # Populate Table
        table = self.query_one("#tasks-data-table", DataTable)
        table.clear()
        for t in tasks:
            # Rich styling for Status Pill
            color = self.get_status_style(t.status)
            status_pill = Text(f" {t.status} ", style=f"bold black on {color}")
            
            # Rich styling for Priority
            p_style = "bold red" if t.priority >= 4 else "white"
            priority = Text(str(t.priority), style=p_style)

            table.add_row(
                str(t.id), 
                status_pill, 
                t.title, 
                t.assignee, 
                priority, 
                str(t.due_date), 
                key=str(t.id)
            )

        # Populate Cards
        card_list = self.query_one("#card-list-container", Container)
        card_list.remove_children()
        for t in tasks:
            card_list.mount(TaskCard(t))

    @on(DataTable.RowSelected)
    def on_table_row_selected(self, event: DataTable.RowSelected) -> None:
        task_id = int(event.row_key.value)
        self.show_details(task_id)

    @on(TaskCard.Selected)
    def on_card_selected(self, message: TaskCard.Selected) -> None:
        self.query_one(ItemDetailPanel).render_task(message.task)

    @work
    async def show_details(self, task_id: int):
        vm = TasksViewModel()
        task = await vm.get_task_by_id(task_id)
        if task:
             self.query_one(ItemDetailPanel).render_task(task)
