import asyncio
from tuitask.db.engine import get_session
from tuitask.db.crud import projects
from sqlmodel.ext.asyncio.session import AsyncSession

async def verify():
    print("Verifying Hierarchy...")
    # Trigger App init logic (or manual init)
    from tuitask.db.engine import init_db
    from tuitask.viewmodels.tasks_viewmodel import TasksViewModel
    
    await init_db()
    vm = TasksViewModel()
    await vm.seed_sample_data()
    
    async for session in get_session():
        projs = await projects.get_all_projects(session)
        print(f"Projects found: {len(projs)}")
        for p in projs:
            p_loaded = await projects.get_project_with_phases(session, p.id)
            print(f"Project: {p_loaded.name} [Loc: {p_loaded.location}, TZ: {p_loaded.timezone}]")
            print(f"  Description: {p_loaded.description}")
            print(f"  Progress: {p_loaded.progress}%")
            
            for phase in p_loaded.phases:
                print(f"  Phase: {phase.name} (Order {phase.order}) - {phase.progress}% done")
                print(f"    Desc: {phase.description}")

if __name__ == "__main__":
    try:
        asyncio.run(verify())
    except Exception as e:
        print(f"Error: {e}")
