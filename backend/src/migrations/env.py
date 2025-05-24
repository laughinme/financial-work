import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# from core.config import Config
from database.relational_db.tables import *
from database.relational_db.tables.table_base import Base
from database.relational_db.database_configuration import DatabaseConfiguration
from database.relational_db.enums import AvailableDatabaseLibraries, AvailableDatabases


db_config = DatabaseConfiguration()
DATABASE_URL = db_config.create_database_url(
    AvailableDatabases.POSTGRESQL, 
    AvailableDatabaseLibraries.ASYNCPG
)
print(DATABASE_URL)

# settings = Config()
# DATABASE_URL = settings.DB_URL
# print(DATABASE_URL)

# Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

fileConfig(config.config_file_name)
target_metadata = Base.metadata
print("Tables in metadata:", list(target_metadata.tables.keys()))


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:

        def do_migrations(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_migrations)


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())
        

run_migrations()