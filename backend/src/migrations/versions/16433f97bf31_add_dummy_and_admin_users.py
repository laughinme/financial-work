"""add dummy and admin users

Revision ID: 16433f97bf31
Revises: a8f06096de2d
Create Date: 2025-06-29 18:56:33.250163

"""
from typing import Sequence, Union
from decimal import Decimal
from datetime import datetime, UTC
import uuid
import bcrypt

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16433f97bf31'
down_revision: Union[str, None] = 'a8f06096de2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def _insert_user(
    *,
    user_id: uuid.UUID,
    secure_code: str,
    email: str,
    password_plain: str,
    display_name: str,
    first_name: str,
    last_name: str,
    role: str,
    verified: bool = True,
) -> None:
    """Helper to insert a user row plus matching identity (provider=PASSWORD)."""
    password_hash: bytes = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt())

    # users -------------------------------------------------------------
    user_sql = """
        INSERT INTO users (
            id, secure_code, email, password_hash, allow_password_login,
            display_name, first_name, last_name, avatar_url,
            role, verified, banned, stripe_onboarding_completed
        )
        VALUES (
            :id, :secure_code, :email, :password_hash, TRUE,
            :display_name, :first_name, :last_name, NULL,
            CAST(:role AS role), :verified, FALSE, FALSE
        );
    """
    op.execute(
        sa.text(user_sql).bindparams(
            id=user_id,
            secure_code=secure_code,
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            first_name=first_name,
            last_name=last_name,
            role=role,
            verified=verified,
        )
    )

    # identities --------------------------------------------------------
    identity_sql = """
        INSERT INTO identities (
            id, user_id, provider, external_id, meta
        ) VALUES (
            :id, :user_id, CAST(:provider AS provider), :external_id,
            '{"is_email": true}'::jsonb
        );
    """
    op.execute(
        sa.text(identity_sql).bindparams(
            id=uuid.uuid4(),
            user_id=user_id,
            provider="PASSWORD",
            external_id=email,
        )
    )


def upgrade() -> None:
    """Seed admin & dummy users plus dummy USD wallet."""
    # --- admin ---------------------------------------------------------
    _insert_user(
        user_id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
        secure_code="supersecret",
        email="admin@example.com",
        password_plain="adminpassword",
        display_name="Administrator",
        first_name="Admin",
        last_name="User",
        role="ADMIN",
        verified=True,
    )

    # --- dummy guest ---------------------------------------------------
    dummy_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    _insert_user(
        user_id=dummy_user_id,
        secure_code="supersecret",
        email="dummy@user.com",
        password_plain="dummy",
        display_name="Dummy",
        first_name="Dumb",
        last_name="Master",
        role="GUEST",
        verified=False,
    )

    # wallet for dummy --------------------------------------------------
    wallet_sql = """
        INSERT INTO wallets (user_id, currency, balance, locked)
        VALUES (:user_id, :currency, :balance, :locked);
    """
    op.execute(
        sa.text(wallet_sql).bindparams(
            user_id=dummy_user_id,
            currency="USD",
            balance=Decimal("0"),
            locked=Decimal("0"),
        )
    )


def downgrade() -> None:
    """Remove seeded users, identities and wallet rows."""
    admin_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    dummy_id = uuid.UUID("00000000-0000-0000-0000-000000000001")

    # delete in dependency-safe order
    op.execute(sa.text("DELETE FROM wallets WHERE user_id = :uid"), {"uid": dummy_id})
    op.execute(sa.text("DELETE FROM identities WHERE user_id IN (:a, :b)"), {"a": admin_id, "b": dummy_id})
    op.execute(sa.text("DELETE FROM users WHERE id IN (:a, :b)"), {"a": admin_id, "b": dummy_id})
