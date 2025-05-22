from sqlalchemy.orm import mapped_column
from sqlalchemy import UUID, String

import uuid_utils

from ..table_base import TableBase


class UsersTable(TableBase):
    __tablename__ = "users_table"

    id = mapped_column(UUID(as_uuid=True), default=uuid_utils.uuid7, primary_key=True)

    email = mapped_column(String, unique=True)
    phone_number = mapped_column(String, unique=True)

    password = mapped_column(String, nullable=False)
    secure_code = mapped_column(String, nullable=False)
    secret = mapped_column(String)
