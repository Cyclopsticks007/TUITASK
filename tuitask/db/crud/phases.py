from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from tuitask.models.phase import Phase

async def create_phase(session: AsyncSession, phase: Phase) -> Phase:
    session.add(phase)
    await session.commit()
    await session.refresh(phase)
    return phase

async def get_phases_by_project(session: AsyncSession, project_id: int) -> list[Phase]:
    statement = select(Phase).where(Phase.project_id == project_id).order_by(Phase.order)
    result = await session.exec(statement)
    return list(result.all())
