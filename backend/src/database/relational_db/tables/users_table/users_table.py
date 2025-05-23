import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, String

from ..table_base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    password: Mapped[str] = mapped_column(String, nullable=False)
    secure_code: Mapped[str] = mapped_column(String, nullable=False)
    secret: Mapped[str] = mapped_column(String)
