import uuid
import secrets

from passlib.context import CryptContext
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import BYTEA

from domain.users import Role
from ..table_base import Base
from ..mixins import TimestampMixin


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    secure_code: Mapped[str] = mapped_column(String, nullable=False)
    
    email: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    password_hash: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    allow_password_login: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.GUEST)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    stripe_account_id: Mapped[str | None] = mapped_column(String, nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    stripe_onboarding_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    identities: Mapped[list["Identity"]] = relationship(  # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
    holdings = relationship("Holding", back_populates="user", lazy="selectin")
    unit_issues = relationship("UnitIssue", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    wallets: Mapped[list["Wallet"]] = relationship(back_populates='user') # type: ignore
    
    
    @staticmethod
    def _gen_secure_code() -> str:
        return secrets.token_urlsafe(48)
    
    @staticmethod
    def _gen_password() -> str:
        return secrets.token_urlsafe(24)

    @classmethod
    def create(cls) -> "User":
        raw_password = cls._gen_password()
        password_hash = pwd_context.hash(raw_password).encode()

        return cls(
            secure_code=cls._gen_secure_code(),
            password_hash=password_hash,
            allow_password_login=False
        )
