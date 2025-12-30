from __future__ import annotations

from tuitask.db.engine import get_session
from tuitask.db.crud import tasks as task_crud
from tuitask.models.task import Task
from datetime import date, timedelta

class TasksViewModel:
    async def get_all_tasks(self) -> list[Task]:
        async for session in get_session():
            return await task_crud.get_all_tasks(session)
        return []

    async def get_task_by_id(self, task_id: int) -> Task | None:
        async for session in get_session():
            return await task_crud.get_task(session, task_id)
        return None

    async def add_task(self, task: Task):
        async for session in get_session():
            await task_crud.create_task(session, task)

    async def get_hierarchy(self) -> list["Project"]:
        # Import inside method or at top if Project is available
        from tuitask.models.project import Project
        from tuitask.db.crud import projects as project_crud
        async for session in get_session():
            return await project_crud.get_full_hierarchy(session)
        return []

    async def add_project(self, name: str, description: str = "") -> Project:
        """Create a new project."""
        from tuitask.db.crud import projects as project_crud
        from tuitask.db.session import get_db_context
        
        async with get_db_context() as db:
            return await project_crud.create_project(db, name, description)

    async def add_phase(self, project_id: int, name: str) -> Phase:
        """Create a new phase in a project."""
        from tuitask.db.crud import projects as project_crud
        from tuitask.db.session import get_db_context
        
        async with get_db_context() as db:
            return await project_crud.create_phase(db, project_id, name)
            
    async def seed_sample_data(self):
        """Seeds initial data if DB is empty."""
        from tuitask.db.crud import projects as project_crud
        from tuitask.db.crud import phases as phase_crud
        from tuitask.models.project import Project, ProjectLocation
        from tuitask.models.phase import Phase
        
        existing = await self.get_all_tasks()
        if existing:
            return

        print("Seeding hierarchy data...")
        async for session in get_session():
            # Create Project
            proj = Project(
                name="Website Redesign", 
                location=ProjectLocation.LOCAL,
                timezone="UTC",
                description="Overhaul of the main corporate website."
            )
            await project_crud.create_project(session, proj)
            
            # Create Phases
            p1 = Phase(name="Planning", description="Requirements gathering", order=1, project_id=proj.id)
            p2 = Phase(name="Development", description="Coding and implementation", order=2, project_id=proj.id)
            p3 = Phase(name="Testing", description="QA and UAT", order=3, project_id=proj.id)
            
            await phase_crud.create_phase(session, p1)
            await phase_crud.create_phase(session, p2)
            await phase_crud.create_phase(session, p3)
            
            # Create Tasks linked to Phases
            sample_tasks = [
                Task(title="Ship MVP login flow", status="Started", assignee="Ada", priority=4, tags_str="auth,ui", requires_signoff=True, due_date=date.today() + timedelta(days=2), phase_id=p2.id),
                Task(title="Set up Pi-hosted instance", status="Assigned", assignee="Sam", priority=3, tags_str="hosting,infra", due_date=date.today() + timedelta(days=5), phase_id=p2.id),
                Task(title="Draft task card UI", status="Needs sign-off", assignee="Riley", priority=5, tags_str="design,ui", requires_signoff=True, due_date=date.today() + timedelta(days=1), phase_id=p1.id),
                Task(title="Connect AI key store", status="Not assigned", assignee="Unassigned", priority=2, tags_str="ai,keys", due_date=date.today() + timedelta(days=8), phase_id=p2.id),
            ]
            
            for t in sample_tasks:
                await task_crud.create_task(session, t)
