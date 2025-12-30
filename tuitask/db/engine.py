from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# DB Config
DATABASE_URL = "sqlite+aiosqlite:///tuitask.db"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async def init_db():
    async with engine.begin() as conn:
        # Import models to ensure they are registered in metadata
        from tuitask.models.project import Project
        from tuitask.models.phase import Phase
        from tuitask.models.task import Task
        
        # Create all tables defined in SQLModel metadata
        # await conn.run_sync(SQLModel.metadata.drop_all) # Uncomment to reset
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
