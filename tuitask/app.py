from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
    TabbedContent,
    TabPane,
)


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


class LoginScreen(Screen):
    BINDINGS = [("enter", "submit", "Sign in")]

    def compose(self) -> ComposeResult:
        yield Container(
            Static("TUITASK", classes="login-title"),
            Static("Fast local task management for teams.", classes="login-subtitle"),
            Input(placeholder="Username", id="username"),
            Input(placeholder="Access key (local)", password=True, id="access_key"),
            Static("Auth mode", classes="login-label"),
            Horizontal(
                Button("Simple local login", id="auth-simple", classes="toggle on"),
                Button("Server auth", id="auth-server", classes="toggle"),
                classes="toggle-row",
            ),
            Static("Storage mode", classes="login-label"),
            Horizontal(
                Button("Local (offline)", id="storage-local", classes="toggle on"),
                Button("Server (realtime)", id="storage-server", classes="toggle"),
                classes="toggle-row",
            ),
            Button("Launch workspace", id="login", classes="primary"),
            classes="login-card",
        )

    @on(Button.Pressed, "#login")
    def handle_login(self) -> None:
        self.app.action_submit()

    @on(Button.Pressed)
    def handle_toggle(self, event: Button.Pressed) -> None:
        if not event.button.id:
            return
        if event.button.id in {"auth-simple", "auth-server"}:
            self._set_toggle_group("auth", event.button.id)
        if event.button.id in {"storage-local", "storage-server"}:
            self._set_toggle_group("storage", event.button.id)

    def _set_toggle_group(self, group: str, active_id: str) -> None:
        ids = {
            "auth": ["auth-simple", "auth-server"],
            "storage": ["storage-local", "storage-server"],
        }[group]
        for button_id in ids:
            button = self.query_one(f"#{button_id}", Button)
            button.remove_class("on")
        self.query_one(f"#{active_id}", Button).add_class("on")


class DashboardPanel(Static):
    def compose(self) -> ComposeResult:
        yield Static("Live Operations", classes="panel-title")
        yield Static("• 4 tasks due this week")
        yield Static("• 2 support tickets waiting on QA")
        yield Static("• Rank XP +120 from yesterday")
        yield Static("• Server load stable (Pi 4 @ 18%)")


class TaskListPanel(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Static("Task List", classes="panel-title")
        task_list = ListView(classes="task-list", id="task-list")
        for task in SAMPLE_TASKS:
            item = ListItem(
                Label(
                    f"{task.title}  ·  {task.status}  ·  P{task.priority}  ·  {task.due_date:%b %d}"
                )
            )
            task_list.append(item)
        yield task_list


class TaskCardPanel(Vertical):
    active_task: reactive[Task | None] = reactive(SAMPLE_TASKS[0])

    def compose(self) -> ComposeResult:
        yield Static("Task Card", classes="panel-title")
        yield Static("", id="task-card-content")

    def watch_active_task(self, task: Task | None) -> None:
        content = self.query_one("#task-card-content", Static)
        if not task:
            content.update("Select a task to see details.")
            return
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


class CalendarPanel(Static):
    def compose(self) -> ComposeResult:
        yield Static("Calendar", classes="panel-title")
        yield Static("Upcoming milestones")
        yield Static("• Mon: Sprint demo")
        yield Static("• Wed: Ops review")
        yield Static("• Fri: Deploy lightweight server")


class ProfilePanel(Static):
    def compose(self) -> ComposeResult:
        yield Static("User Profile", classes="panel-title")
        yield Static("Handle: @operator")
        yield Static("Rank: Architect (XP 2,480)")
        yield Static("Active streak: 12 days")
        yield Static("Badges: Velocity · Mentor · Builder")


class HostingPanel(Static):
    def compose(self) -> ComposeResult:
        yield Static("Server Hosting", classes="panel-title")
        yield Static("Mode: Self-hosted / Raspberry Pi")
        yield Static("Status: Online • 4 active users")
        yield Static("Sync: Async realtime")
        yield Static("Database: SQLite (local cache)")


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(classes="app-body"):
            with Vertical(classes="side-panel"):
                yield Static("Workspace", classes="nav-title")
                yield Button("Dashboard", id="nav-dashboard", classes="nav-button")
                yield Button("Tasks", id="nav-tasks", classes="nav-button")
                yield Button("Calendar", id="nav-calendar", classes="nav-button")
                yield Button("Profile", id="nav-profile", classes="nav-button")
                yield Button("Hosting", id="nav-hosting", classes="nav-button")
                yield Button("Sign out", id="nav-signout", classes="nav-button ghost")
            with TabbedContent(id="main-tabs"):
                with TabPane("Dashboard", id="dashboard"):
                    yield DashboardPanel(classes="panel")
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
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#main-tabs", TabbedContent).active = "dashboard"

    @on(Button.Pressed)
    def handle_nav(self, event: Button.Pressed) -> None:
        target_map = {
            "nav-dashboard": "dashboard",
            "nav-tasks": "tasks",
            "nav-calendar": "calendar",
            "nav-profile": "profile",
            "nav-hosting": "hosting",
        }
        if event.button.id == "nav-signout":
            self.app.push_screen(LoginScreen())
            return
        target = target_map.get(event.button.id)
        if target:
            self.query_one("#main-tabs", TabbedContent).active = target

    @on(ListView.Highlighted)
    def handle_task_focus(self, event: ListView.Highlighted) -> None:
        if event.list_view.id != "task-list":
            return
        if event.index is None:
            return
        task = SAMPLE_TASKS[event.index]
        self.query_one(TaskCardPanel).active_task = task


class TuiTaskApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "TUITASK"
    BINDINGS = [("ctrl+q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())

    def action_submit(self) -> None:
        self.pop_screen()
        self.push_screen(MainScreen())


def run() -> None:
    TuiTaskApp().run()


if __name__ == "__main__":
    run()
