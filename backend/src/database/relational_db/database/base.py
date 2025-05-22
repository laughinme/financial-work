from abc import ABC, abstractmethod
from enum import Enum

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from ..database_configuration import DatabaseConfiguration


class BaseRelationalDatabase(ABC):
    """
    Parent class for any other relational databases classes such as:
        ⌞PostgreSQL\n
        ⌞MySQL\n
        ⌞AioSQLite\n
    and any other relational database classes.
    """

    def __init__(self, database_type: Enum, database_library: Enum):
        self.cfg = DatabaseConfiguration()
        self.engine = create_async_engine(
            self.cfg.create_database_url(
                database_type,
                database_library
            )
        )
        self.Session = async_sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    @abstractmethod
    async def create_tables(self):
        """
        Function that created all project tables.
        """
