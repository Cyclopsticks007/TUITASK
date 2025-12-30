from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Button, ContentSwitcher
from textual.app import ComposeResult
from textual import on

from tuitask.components.navigation import TopNav
from tuitask.views.dashboard import DashboardView
# Switch to V3 Tasks View
from tuitask.ui.screens.tasks import TasksScreen
from tuitask.ui.screens.create_modal import CreateModal

class MainScreen(Screen):
    BINDINGS = [
        ("a", "add_task", "Add Task"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield TopNav(id="top-nav")
        with ContentSwitcher(initial="dashboard", id="content-switcher"):
            yield DashboardView(id="dashboard")
            yield TasksScreen(id="tasks")
    
    def on_mount(self) -> None:
        pass

    @on(Button.Pressed)
    def handle_nav(self, event: Button.Pressed) -> None:
        import logging
        logging.debug(f"Nav Button Pressed: {event.button.id}")
        if event.button.id == "tab-home":
            self.query_one("#content-switcher", ContentSwitcher).current = "dashboard"
            self.update_nav_state("tab-home")
        elif event.button.id == "tab-tasks":
            # Switch to tasks (V3)
            self.query_one("#content-switcher", ContentSwitcher).current = "tasks"
            self.update_nav_state("tab-tasks")
            
            # Optional: trigger refresh on TasksScreen
            # self.query_one(TasksScreen).load_hierarchy()
            
        elif event.button.id == "tab-manager":
            pass
    
    def update_nav_state(self, active_id: str):
        for btn in self.query("TopNav .tab"): 
            if btn.id == active_id:
                btn.add_class("active")
                btn.variant = "primary"
            else:
                btn.remove_class("active")
                btn.variant = "default"

    def action_add_task(self) -> None:
        try:
            self.query_one(TasksScreen).open_create_modal(kind="task")
        except Exception:
            self.app.push_screen(CreateModal(), callback=self.on_task_added)

    def on_task_added(self, result = None) -> None:
        if result:
            self.app.notify(f"Created: {result.get('title', 'Item')}")
            # Refresh V3 Tasks View
            try:
                self.query_one(TasksScreen).load_hierarchy()
                self.query_one(TasksScreen).load_tasks()
            except:
                pass
