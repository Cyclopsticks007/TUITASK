from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from tuitask.models.phase import Phase

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str = "Assigned" # Kept for general status (e.g. Blocked), distinct from Phase? Or maybe redundant.
    assignee: str = "Unassigned"
    priority: int = 3
    
    # Hierarchy
    phase_id: Optional[int] = Field(default=None, foreign_key="phase.id")
    phase: Optional["Phase"] = Relationship(back_populates="tasks")
    
    # Dates
    start_date: date = Field(default_factory=date.today)
    due_date: date = Field(default_factory=date.today)
    
    # Simplified for SQL MVP (Storing lists as comma strings or separate tables later)
    tags_str: str = "" 
    links_str: str = ""
    requires_signoff: bool = False

    @property
    def task_id(self) -> int:
        return self.id if self.id else 0

    @property
    def tags(self) -> tuple[str, ...]:
        return tuple(self.tags_str.split(",")) if self.tags_str else ()

    @property
    def links(self) -> tuple[int, ...]:
        # Simple parsing for MVP
        if not self.links_str:
            return ()
        try:
            return tuple(int(x) for x in self.links_str.split(",") if x.strip())
        except ValueError:
            return ()


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

# No global SAMPLE_TASKS, database will replace it.
