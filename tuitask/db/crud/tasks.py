from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from tuitask.models.task import Task
from typing import Optional

async def create_task(session: AsyncSession, task: Task) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(session: AsyncSession, task_id: int) -> Optional[Task]:
    return await session.get(Task, task_id)

async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.exec(select(Task))
    return list(result.all())

async def update_task(session: AsyncSession, task_id: int, task_update: Task) -> Optional[Task]:
    db_task = await session.get(Task, task_id)
    if not db_task:
        return None
    
    # Update fields (simplistic mapping for now)
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
        
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def delete_task(session: AsyncSession, task_id: int) -> bool:
    task = await session.get(Task, task_id)
    if not task:
        return False
    await session.delete(task)
    await session.commit()
    return True
