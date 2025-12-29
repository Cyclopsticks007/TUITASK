from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

import calendar
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll, Grid
from textual.reactive import reactive
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Button,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
    TabbedContent,
    TabPane,
    Tree,
)

class CalendarWidget(Container):
    """A custom calendar widget that requires a grid layout in CSS."""
    
    def compose(self) -> ComposeResult:
        today = date.today()
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
        month_name = calendar.month_name[today.month]
        year = today.year
        
        # Get the first and last day of the current week for the period label
        # Find what week we're in
        start_of_month = date(year, today.month, 1)
        end_of_month = date(year, today.month, calendar.monthrange(year, today.month)[1])
        
        # Simple period display - just show the month range
        period_text = f"<<< {start_of_month.day} {month_name[:3]} - {end_of_month.day} {month_name[:3]} >>>"
        
        # Header with date range
        yield Label(period_text, classes="calendar-title")
        
        # Grid Container
        with Container(classes="calendar-internal-grid"):
            # Weekday Headers - SINGLE LETTERS
            for day in ["S", "M", "T", "W", "T", "F", "S"]:
                yield Label(day, classes="calendar-day-header")
            
            # Days
            for d in cal.itermonthdates(year, today.month):
                day_classes = ["calendar-day"]
                
                if d == today:
                    day_classes.append("today")
                elif d.month != today.month:
                    day_classes.append("other-month")
                elif d < today:
                    day_classes.append("passed")
                else:
                    day_classes.append("future")
                    
                yield Label(str(d.day), classes=" ".join(day_classes))

class TaskCreationScreen(ModalScreen):
    """A modal screen for creating new tasks."""

    def compose(self) -> ComposeResult:
        with Container(classes="modal-container"):
            yield Label("Create New Task", classes="modal-title")
            yield Input(placeholder="Task Title", id="task_title")
            yield Input(placeholder="Assignee", id="task_assignee")
            yield Input(placeholder="Priority (1-5)", id="task_priority")
            yield Label("Status: Assigned (Default)", id="status_label")
            with Horizontal():
                yield Button("Save", variant="primary", id="save_task")
                yield Button("Cancel", id="cancel_task")

    @on(Button.Pressed, "#cancel_task")
    def cancel(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#save_task")
    def save(self) -> None:
        title = self.query_one("#task_title", Input).value
        assignee = self.query_one("#task_assignee", Input).value
        priority_str = self.query_one("#task_priority", Input).value
        
        if not title:
            self.app.notify("Title is required", severity="warning")
            return
            
        try:
            priority = int(priority_str)
        except ValueError:
            priority = 3
            
        new_task = Task(
            task_id=len(SAMPLE_TASKS) + 1,
            title=title,
            start_date=date.today(),
            due_date=date.today() + timedelta(days=7),
            status="Assigned",
            assignee=assignee or "Unassigned",
            priority=priority,
            tags=(),
            links=(),
            requires_signoff=False
        )
        SAMPLE_TASKS.append(new_task)
        self.app.notify(f"Task '{title}' created!")
        self.dismiss(True)


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    start_date: date
    due_date: date
    status: str
    assignee: str
    priority: int
    tags: tuple[str, ...]
    links: tuple[int, ...]
    requires_signoff: bool


class StorageMode(str, Enum):
    LOCAL = "Local (offline)"
    SERVER = "Server (realtime)"


class AuthMode(str, Enum):
    SIMPLE = "Simple local login"
    SERVER = "Server auth"


def velocity_points(task: Task, today: date | None = None) -> int:
    today = today or date.today()
    base = task.priority * 10
    days_until_due = (task.due_date - today).days
    if task.status.lower() == "completed":
        return base + max(0, days_until_due) * 2
    if days_until_due < 0:
        return max(0, base + days_until_due * 3)
    urgency_bonus = max(0, 10 - days_until_due)
    return base + urgency_bonus


SAMPLE_TASKS = [
    Task(
        1,
        "Ship MVP login flow",
        date.today() - timedelta(days=1),
        date.today() + timedelta(days=2),
        "Started",
        "Ada",
        priority=4,
        tags=("auth", "ui"),
        links=(3,),
        requires_signoff=True,
    ),
    Task(
        2,
        "Set up Pi-hosted instance",
        date.today(),
        date.today() + timedelta(days=5),
        "Assigned",
        "Sam",
        priority=3,
        tags=("hosting", "infra"),
        links=(),
        requires_signoff=False,
    ),
    Task(
        3,
        "Draft task card UI",
        date.today() - timedelta(days=2),
        date.today() + timedelta(days=1),
        "Needs sign-off",
        "Riley",
        priority=5,
        tags=("design", "ui"),
        links=(),
        requires_signoff=True,
    ),
    Task(
        4,
        "Connect AI key store",
        date.today(),
        date.today() + timedelta(days=8),
        "Not assigned",
        "Unassigned",
        priority=2,
        tags=("ai", "keys"),
        links=(2,),
        requires_signoff=False,
    ),
]


import json
import os
from pathlib import Path


class UserStorage:
    def __init__(self, filename: str = "users.json"):
        self.path = Path(filename)
        self.users = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text())
        except (json.JSONDecodeError, IOError):
            return {}

    def _save(self):
        self.path.write_text(json.dumps(self.users))

    def create_user(self, username: str, access_key: str):
        self.users[username] = access_key
        self._save()

    def authenticate(self, username: str, access_key: str) -> bool:
        return self.users.get(username) == access_key

    def has_users(self) -> bool:
        return len(self.users) > 0


class LoginScreen(Screen):
    BINDINGS = [("enter", "submit", "Sign in")]
    storage = UserStorage()

    def compose(self) -> ComposeResult:
        has_users = self.storage.has_users()
        title = "TUITASK"
        subtitle = "Fast local task management for teams."
        
        if not has_users:
            label = "Initialize Workspace"
            button_text = "Create Admin Account"
            fields = [
                Input(placeholder="Choose Username", id="username"),
                Input(placeholder="Create Access Key", password=True, id="access_key"),
                Input(placeholder="Confirm Access Key", password=True, id="confirm_key"),
            ]
        else:
            label = "Welcome Back"
            button_text = "Launch Workspace"
            fields = [
                Input(placeholder="Username", id="username"),
                Input(placeholder="Access key", password=True, id="access_key"),
            ]

        yield Container(
            Static(title, classes="login-title"),
            Static(subtitle, classes="login-subtitle"),
            Static(label, classes="login-label-center"),
            *fields,
            Button(button_text, id="login", classes="primary"),
            classes="login-card",
        )

    def on_mount(self) -> None:
        self.query_one("#username").focus()

    @on(Input.Submitted)
    def handle_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "username":
            self.query_one("#access_key").focus()
        elif event.input.id == "access_key":
             # Trigger login logic directly
             self.handle_login()
        elif event.input.id == "confirm_key":
             self.handle_login()

    @on(Button.Pressed, "#login")
    def handle_login(self) -> None:
        username = self.query_one("#username", Input).value
        access_key = self.query_one("#access_key", Input).value
        
        if not self.storage.has_users():
            # Registration flow
            confirm_key = self.query_one("#confirm_key", Input).value
            if not username or not access_key:
                self.app.notify("Username and key are required.", severity="error")
                return
            if access_key != confirm_key:
                self.app.notify("Access keys do not match.", severity="error")
                return
            
            self.storage.create_user(username, access_key)
            self.app.notify(f"Account created for {username}!", severity="information")
            # Re-mount to show login screen or just proceed
            self.app.action_submit()
        else:
            # Login flow
            if self.storage.authenticate(username, access_key):
                self.app.action_submit()
            else:
                self.app.notify("Invalid credentials.", severity="error")



class DashboardPanel(Static):
    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing DashboardPanel")
        try:
            yield Static("Live Operations", classes="panel-title")
            yield Static("• 4 tasks due this week")
            yield Static("• 2 support tickets waiting on QA")
            yield Static("• Rank XP +120 from yesterday")
            yield Static("• Server load stable (Pi 4 @ 18%)")
        except Exception as e:
            logging.exception("Error composing DashboardPanel")
            yield Static(f"Error loading dashboard: {e}")


class TaskListPanel(VerticalScroll):
    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing TaskListPanel")
        try:
            self.border_title = "Task List"
            task_list = ListView(classes="task-list", id="task-list")
            if not SAMPLE_TASKS:
                task_list.append(ListItem(Label("No tasks available")))
            else:
                for task in SAMPLE_TASKS:
                    item = ListItem(
                        Label(
                            f"{task.title}  ·  {task.status}  ·  P{task.priority}  ·  {task.due_date:%b %d}"
                        )
                    )
                    task_list.append(item)
            yield task_list
        except Exception as e:
            logging.exception("Error composing TaskListPanel")
            yield Static(f"Error loading task list: {e}")


class TaskCardPanel(Vertical):
    active_task: reactive[Task | None] = reactive(None)

    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing TaskCardPanel")
        self.border_title = "Task Card"
        yield Static("", id="task-card-content")

    def on_mount(self) -> None:
        import logging
        logging.debug("Mounting TaskCardPanel")
        # Initialize with first task if available and not already set
        if self.active_task is None and SAMPLE_TASKS:
             self.active_task = SAMPLE_TASKS[0]
        self.watch_active_task(self.active_task)

    def watch_active_task(self, task: Task | None) -> None:
        if not self.is_mounted:
            return
        
        try:
            content = self.query_one("#task-card-content", Static)
        except Exception:
            return

        if not task:
            content.update("Select a task to see details.")
            return
        
        try:
            velocity = velocity_points(task)
            content.update(
                "\n".join(
                    [
                        f"Title: {task.title}",
                        f"Status: {task.status}",
                        f"Start: {task.start_date:%A, %b %d}",
                        f"Due: {task.due_date:%A, %b %d}",
                        f"Assignee: {task.assignee}",
                        f"Priority: {task.priority}",
                        f"Tags: {', '.join(task.tags) if task.tags else 'None'}",
                        f"Links: {', '.join(str(link) for link in task.links) if task.links else 'None'}",
                        f"Velocity points: {velocity}",
                        f"Sign-off required: {'Yes' if task.requires_signoff else 'No'}",
                    ]
                )
            )
        except Exception as e:
             import logging
             logging.exception("Error updating task card")
             content.update(f"Error displaying task: {e}")


class CalendarPanel(Static):
    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing CalendarPanel")
        self.border_title = "Calendar"
        yield Static("Upcoming milestones")
        yield Static("• Mon: Sprint demo")
        yield Static("• Wed: Ops review")
        yield Static("• Fri: Deploy lightweight server")


class ProfilePanel(Static):
    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing ProfilePanel")
        self.border_title = "User Profile"
        yield Static("Handle: @operator")
        yield Static("Rank: Architect (XP 2,480)")
        yield Static("Active streak: 12 days")
        yield Static("Badges: Velocity · Mentor · Builder")


class HostingPanel(Static):
    def compose(self) -> ComposeResult:
        import logging
        logging.debug("Composing HostingPanel")
        self.border_title = "Server Hosting"
        yield Static("Mode: Self-hosted / Raspberry Pi")
        yield Static("Status: Online • 4 active users")
        yield Static("Sync: Async realtime")
        yield Static("Database: SQLite (local cache)")


class MainScreen(Screen):
    BINDINGS = [
        ("a", "add_task", "Add Task"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="app-frame"):
            with Container(classes="app-body"):
                with Vertical(classes="side-panel"):
                    yield Static("TUITASK", classes="nav-title")
                    nav_tree = Tree("Navigation", id="nav-tree")
                    nav_tree.root.expand()
                    nav_tree.root.add_leaf("Dashboard", data="dashboard")
                    nav_tree.root.add_leaf("Tasks", data="tasks")
                    nav_tree.root.add_leaf("Calendar", data="calendar")
                    nav_tree.root.add_leaf("Profile", data="profile")
                    nav_tree.root.add_leaf("Hosting", data="hosting")
                    nav_tree.root.add_leaf("Sign Out", data="signout")
                    yield nav_tree
                
                with Container(id="main-container"):
                    with TabbedContent(id="main-tabs"):
                        with TabPane("Dashboard", id="dashboard"):
                            with Container(classes="dashboard-grid"):
                                with Vertical(classes="module-container") as panel:
                                    panel.border_title = "Live Operations"
                                    yield Vertical(
                                        Horizontal(
                                            Static("Due Soon: ", classes="stat-label"),
                                            Static("4", classes="stat-value"),
                                            classes="stat-row",
                                        ),
                                        Horizontal(
                                            Static("Open Tickets: ", classes="stat-label"),
                                            Static("2", classes="stat-value"),
                                            classes="stat-row",
                                        ),
                                        Horizontal(
                                            Static("Team Velocity: ", classes="stat-label"),
                                            Static("142", classes="stat-value"),
                                            classes="stat-row",
                                        ),
                                    )
                                with Vertical(classes="module-container panel--raised") as panel:
                                    panel.border_title = "Calendar"
                                    yield CalendarWidget(classes="calendar-widget")
                                with Vertical(classes="module-container") as panel:
                                    panel.border_title = "Recent Activity"
                                    yield Static("• @operator logged in")
                                    yield Static("• Task #3 sign-off requested")
                                    yield Static("• Connection stable")
                                with Vertical(classes="module-container") as panel:
                                    panel.border_title = "System Status"
                                    yield HostingPanel()
                                    
                        with TabPane("Tasks", id="tasks"):
                            with Horizontal(classes="task-row"):
                                yield TaskListPanel(classes="panel")
                                yield TaskCardPanel(classes="panel")
                        with TabPane("Calendar", id="calendar"):
                            yield CalendarPanel(classes="panel")
                        with TabPane("Profile", id="profile"):
                            yield ProfilePanel(classes="panel")
                        with TabPane("Hosting", id="hosting"):
                            yield HostingPanel(classes="panel")
            yield Footer(id="key-footer")

    def on_mount(self) -> None:
        app_frame = self.query_one("#app-frame")
        app_frame.border_title = "TUITASK v0.1.0-alpha"
        app_frame.border_subtitle = "Local Instance"
        self.query_one("#main-tabs", TabbedContent).active = "dashboard"
        self.query_one("#nav-tree").focus()

    def action_add_task(self) -> None:
        self.app.push_screen(TaskCreationScreen(), callback=self.on_task_added)

    def on_task_added(self, added: bool = False) -> None:
        if added:
            # Refresh task list - simpler is to just recompose or find the list
            try:
                task_list_panel = self.query_one(TaskListPanel)
                # This is a bit brute force, but effective for a demo:
                task_list_panel.query_one("#task-list").remove()
                
                # Re-add list view logic here or similar
                # For now, let's just trigger a notification is enough, 
                # but better to update the UI.
                self.app.switch_screen(MainScreen()) # Brutal refresh
            except Exception:
                pass

    @on(Tree.NodeSelected)
    def handle_tree_nav(self, event: Tree.NodeSelected) -> None:
        target = event.node.data
        if not target:
            return
            
        if target == "signout":
            self.app.switch_screen(LoginScreen())
            return
            
        try:
            self.query_one("#main-tabs", TabbedContent).active = target
        except Exception:
            pass

    @on(ListView.Highlighted)
    def handle_task_focus(self, event: ListView.Highlighted) -> None:
        if event.list_view.id != "task-list":
            return
        if event.index is None:
            return
        if not SAMPLE_TASKS:
            return
        
        try:
            task = SAMPLE_TASKS[event.index]
            self.query_one(TaskCardPanel).active_task = task
        except Exception:
            import logging
            logging.exception("Error handling task focus")


class TuiTaskApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "TUITASK"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("a", "add_task", "Add Task"),
    ]

    def on_mount(self) -> None:
        import logging
        logging.debug("App mounted")
        self.push_screen(LoginScreen())

    def action_add_task(self) -> None:
        # If on MainScreen, trigger its add_task action
        if isinstance(self.screen, MainScreen):
            self.screen.action_add_task()

    def action_submit(self) -> None:
        import logging
        logging.debug("Switching to MainScreen")
        self.switch_screen(MainScreen())


def run() -> None:
    import logging
    logging.basicConfig(filename="tuitask.log", level=logging.DEBUG, filemode='w')
    logging.info("Starting TUITASK")
    try:
        app = TuiTaskApp()
        app.run()
    except Exception:
        logging.exception("Fatal error in TuiTaskApp")
        raise

if __name__ == "__main__":
    run()
