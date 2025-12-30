from textual.app import App
from tuitask.views.main_screen import MainScreen
from tuitask.db.engine import init_db
from tuitask.viewmodels.tasks_viewmodel import TasksViewModel

class TuiTaskApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "TUITASK"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("f10", "quit", "Force Quit"),
        ("a", "add_task", "Add Task"),
    ]

    async def on_mount(self) -> None:
        import logging
        logging.debug("App mounted")
        
        # Init DB
        await init_db()
        
        # Seed Data (Async)
        vm = TasksViewModel()
        await vm.seed_sample_data()
        
        self.push_screen(MainScreen())

    def action_add_task(self) -> None:
        # If on MainScreen, trigger its add_task action
        if isinstance(self.screen, MainScreen):
            self.screen.action_add_task()

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
