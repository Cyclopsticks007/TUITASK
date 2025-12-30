from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from tuitask.models.phase import Phase

class ProjectLocation(str, Enum):
    LOCAL = "local"
    NETWORK = "network"

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location: ProjectLocation = Field(default=ProjectLocation.LOCAL)
    timezone: str = Field(default="UTC")
    description: str = Field(default="")
    
    phases: List["Phase"] = Relationship(back_populates="project")

    @property
    def progress(self) -> int:
        if not self.phases:
            return 0
        total_tasks = 0
        completed_tasks = 0
        for phase in self.phases:
            total_tasks += len(phase.tasks)
            completed_tasks += sum(1 for t in phase.tasks if t.status.lower() == "completed")
        
        if total_tasks == 0:
            return 0
        return int((completed_tasks / total_tasks) * 100)
