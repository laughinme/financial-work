import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, Enum, Boolean

from domain.users import Role
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
    
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.GUEST)
    allow_password_login: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    identities: Mapped[list["Identity"]] = relationship(  # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
    holdings = relationship("Holding", back_populates="user", lazy="selectin")
    unit_issues = relationship("UnitIssue", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    wallets = relationship('Wallet', back_populates='user')
