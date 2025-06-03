import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, Integer, ForeignKey, UniqueConstraint, Enum

from domain.users import Provider
from ..table_base import Base
from ..mixins import TimestampMixin


class AuthProvider(TimestampMixin, Base):
    __tablename__ = "auth_providers"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user"),
    )
    
    user: Mapped["User"] = relationship("User", back_populates="providers") # type: ignore
    
    credentials: Mapped["CredsProvider"] = relationship( # type: ignore
        "CredsProvider",
        uselist=False,
        back_populates="auth_provider",
        cascade="all, delete-orphan",
        single_parent=True
    )
    telegram: Mapped["TelegramProvider"] = relationship( # type: ignore
        "TelegramProvider",
        uselist=False,
        back_populates="auth_provider",
        cascade="all, delete-orphan",
        single_parent=True
    )
