import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, String, Integer, ForeignKey

from ..table_base import Base


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name:  Mapped[str | None] = mapped_column(String, nullable=True)
    username:   Mapped[str | None] = mapped_column(String, nullable=True)
    photo_url:  Mapped[str | None] = mapped_column(String, nullable=True)
