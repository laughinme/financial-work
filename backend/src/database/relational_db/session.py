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

DB_CONFIG = DatabaseConfiguration()
DB_URL = DB_CONFIG.create_database_url(
    AvailableDatabases.POSTGRESQL,
    AvailableDatabaseLibraries.ASYNCPG
)

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns prepared postgres session"""
    async with async_session() as session:
        yield session
