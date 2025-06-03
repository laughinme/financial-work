import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String

from ..table_base import Base
from ..mixins import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    secure_code: Mapped[str] = mapped_column(String, nullable=False)
    
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    
    providers: Mapped[list["AuthProvider"]] = relationship( # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
    holdings = relationship("Holding", back_populates="user", lazy="selectin")
    unit_issues = relationship("UnitIssue", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
