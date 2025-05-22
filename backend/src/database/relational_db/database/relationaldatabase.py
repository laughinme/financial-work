import logging

from .base import BaseRelationalDatabase
from ..tables.table_base import TableBase
from ..enums import AvailableDatabases, AvailableDatabaseLibraries


class RelationalDatabase(BaseRelationalDatabase):
    """
    Class for work with any database engines.
    Can get some Interfaces for work with it.

    Another param is library for work with Database.
    """
    def __init__(self,
                 *interfaces,
                 database_engine: AvailableDatabases = AvailableDatabases.POSTGRESQL,
                 database_library: AvailableDatabaseLibraries = AvailableDatabaseLibraries.ASYNCPG
                 ):
        super().__init__(database_engine, database_library)
        self.interfaces = interfaces
        self.logger = logging.getLogger(__name__)
        for interface in self.interfaces:
            for method_name in dir(interface):
                method = getattr(interface, method_name)
                if "__" not in method_name and callable(method):
                    setattr(self, method_name, self._wrap_method(method))

    def _wrap_method(self, method):
        async def wrapped_method(*args, **kwargs):
            async with self.Session() as session:
                return await method(session=session, *args, **kwargs)
        return wrapped_method

    async def create_tables(self):
        async with self.engine.begin() as connection:
            self.logger.info("Creating Tables...")
            await connection.run_sync(TableBase.metadata.create_all)
            self.logger.info("Tables are successful created!")

    def __getitem__(self, item: str):
        match item:
            case "tables":
                return sorted(
                    [interface.parent_table for interface in self.interfaces],
                    key=lambda x: x.__class__.__name__
                )
            case _:
                raise KeyError("This name is not defined in RelationalDatabase object!")
