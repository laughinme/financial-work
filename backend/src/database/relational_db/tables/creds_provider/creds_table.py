import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, UniqueConstraint, ForeignKey, Integer, Boolean

from ..table_base import Base


class CredsProvider(Base):
    __tablename__ = "credentials_providers"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_providers.id", ondelete="CASCADE"),
        primary_key=True
    )

    is_email: Mapped[bool] = mapped_column(Boolean, default=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # We can add it if we need to
    # secret: Mapped[str] = mapped_column(String)
    
    auth_provider: Mapped["AuthProvider"] = relationship( # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
