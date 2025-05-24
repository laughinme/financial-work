from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey

from ..table_base import Base


class TelegramProvider(Base):
    __tablename__ = "telegram_providers"

    id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("auth_providers.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name:  Mapped[str | None] = mapped_column(String, nullable=True)
    username:   Mapped[str | None] = mapped_column(String, nullable=True)
    photo_url:  Mapped[str | None] = mapped_column(String, nullable=True)

    auth_provider: Mapped["AuthProvider"] = relationship(back_populates="telegram") # type: ignore
