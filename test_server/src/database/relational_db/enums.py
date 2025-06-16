from enum import Enum


class AvailableDatabaseLibraries(Enum):
    """
    Class with available database libraries (just Enum for better typing).
    """
    ASYNCPG = "asyncpg"


class AvailableDatabases(Enum):
    """
    Class with available database types (just Enum for better typing).
    """
    POSTGRESQL = [AvailableDatabaseLibraries.ASYNCPG]
