from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker,
    AsyncSession, 
    AsyncEngine
)

from .database_configuration import DatabaseConfiguration
from .enums import AvailableDatabaseLibraries, AvailableDatabases
from .unit_of_work import UoW


DB_CONFIG = DatabaseConfiguration()
DB_URL = DB_CONFIG.create_database_url(
    AvailableDatabases.POSTGRESQL,
    AvailableDatabaseLibraries.ASYNCPG
)

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)


async def get_uow() -> AsyncGenerator[UoW, None]:
    """Yields Unit of Work instead of raw sessions."""
    async with async_session() as session:
        async with UoW(session) as uow:
            yield uow
