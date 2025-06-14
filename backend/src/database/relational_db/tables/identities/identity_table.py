import uuid
from datetime import datetime

from sqlalchemy import (
    UUID, String, Enum, ForeignKey, Boolean, JSON, UniqueConstraint, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.users import Provider
from ..table_base import Base
from ..mixins import TimestampMixin


class Identity(TimestampMixin, Base):
    __tablename__ = "identities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[Provider] = mapped_column(Enum(Provider), nullable=False)
    external_id: Mapped[str] = mapped_column(String, nullable=False)
    secret_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="identities")  # type: ignore

    __table_args__ = (
        UniqueConstraint("provider", "external_id", name="uq_provider_external"),
    )
