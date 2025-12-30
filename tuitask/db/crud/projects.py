from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from tuitask.models.project import Project

async def create_project(session: AsyncSession, project: Project) -> Project:
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project

async def get_all_projects(session: AsyncSession) -> list[Project]:
    result = await session.exec(select(Project))
    return list(result.all())

async def get_project_with_phases(session: AsyncSession, project_id: int) -> Project | None:
    # Eager load phases AND their tasks for progress calc
    from tuitask.models.phase import Phase
    statement = select(Project).where(Project.id == project_id).options(
        selectinload(Project.phases).selectinload(Phase.tasks)
    )
    result = await session.exec(statement)
    return result.first()

async def get_full_hierarchy(session: AsyncSession) -> list[Project]:
    from tuitask.models.phase import Phase
    statement = select(Project).options(
        selectinload(Project.phases).selectinload(Phase.tasks)
    )
    result = await session.exec(statement)
    return list(result.all())
