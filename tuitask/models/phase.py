from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from tuitask.models.project import Project
    from tuitask.models.task import Task

class Phase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = Field(default="")
    order: int = Field(default=0)
    
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="phases")
    
    tasks: List["Task"] = Relationship(back_populates="phase")

    @property
    def progress(self) -> int:
        if not self.tasks:
            return 0
        completed = sum(1 for t in self.tasks if t.status.lower() == "completed")
        return int((completed / len(self.tasks)) * 100)
