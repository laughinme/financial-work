from typing import Final
from enum import Enum

from .exceptions import InvalidLibraryError


class DatabaseConfiguration:
    """
    ↱ Class that have all database configuration for SQLAlchemy\n
    | <Advanced> | \n
    ↳ Have a function that returning database URL\n
        ↳ Could be used as String.\n
    """
    DB_HOST: Final[str] = "localhost"
    DB_PORT: Final[int] = 5432
    DB_USER: Final[str] = "postgres"
    DB_PASS: Final[str] = "1"
    DB_NAME: Final[str] = "test"

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
