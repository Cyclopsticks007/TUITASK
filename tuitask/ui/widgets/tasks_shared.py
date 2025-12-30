from __future__ import annotations

from dataclasses import dataclass

from tuitask.models.task import Task


@dataclass(frozen=True)
class TaskDisplay:
    task: Task
    project_name: str
    phase_name: str
    project_id: int | None = None
