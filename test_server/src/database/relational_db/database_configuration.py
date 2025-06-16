from typing import Final
from enum import Enum

from core.config import Config
from .exceptions import InvalidLibraryError

config = Config()


class DatabaseConfiguration:
    """
    ↱ Class that have all database configuration for SQLAlchemy\n
    | <Advanced> | \n
    ↳ Have a function that returning database URL\n
        ↳ Could be used as String.\n
    """
    DB_HOST: Final[str] = config.DB_HOST
    DB_PORT: Final[int] = config.DB_PORT
    DB_USER: Final[str] = config.DB_USER
    DB_PASS: Final[str] = config.DB_PASSWORD
    DB_NAME: Final[str] = config.DB_NAME

    def create_database_url(self, type_of_database: Enum, database_library: Enum):
        try:
            if database_library in type_of_database.value:
                return (f"{type_of_database.name.lower()}+{database_library.name.lower()}://"
                        f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
            else:
                raise InvalidLibraryError(
                    f'This database library ({database_library.value}) '
                    f'is not accessible to use! With this database engine'
                    f' you should use one of these libraries:'
                    f' {", ".join([library.value for library in type_of_database.value])}'
                )
        except TypeError as _ex:
            raise ValueError(
                f'Your database is not currently available!'
                f' Please, check the name of the database: "{type_of_database.name}".\n\n'
                f' Also, here is a problem: {_ex}'
            )

    def create_sync_url(self, type_of_database):
        return (f"{type_of_database.name.lower()}://"
                f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
