import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, UniqueConstraint

from ..table_base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    secure_code: Mapped[str] = mapped_column(String, nullable=False)
    
    providers: Mapped[list["AuthProvider"]] = relationship( # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
