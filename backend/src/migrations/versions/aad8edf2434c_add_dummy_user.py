"""add dummy user

Revision ID: aad8edf2434c
Revises: df017e52296d
Create Date: 2025-06-17 17:04:48.555390

"""
from typing import Sequence, Union
from decimal import Decimal
from alembic import op
import sqlalchemy as sa
import uuid
import bcrypt


# revision identifiers, used by Alembic.
revision: str = 'aad8edf2434c'
down_revision: Union[str, None] = 'df017e52296d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add admin user
    user_id = uuid.UUID('00000000-0000-0000-0000-000000000001')
    user_insert_sql = """
        INSERT INTO users (
            id, secure_code, display_name, first_name, last_name, avatar_url, role,
            allow_password_login, banned, stripe_onboarding_completed
        ) VALUES (
            :id, :secure_code, :display_name, :first_name, :last_name, :avatar_url,
            CAST(:role AS role), TRUE, FALSE, FALSE
        );
    """
    op.execute(
        sa.text(user_insert_sql).bindparams(
            id=user_id,
            secure_code="supersecret",
            display_name="Dummy",
            first_name="Dumb",
            last_name="Master",
            avatar_url=None,
            role="GUEST",
        )
    )
    # Add credentials identity for admin user
    hashed_password = bcrypt.hashpw(b'dummy', bcrypt.gensalt()).decode()
    identity_sql = """
        INSERT INTO identities (
            id, user_id, provider, external_id, secret_hash, verified, meta
        ) VALUES (
            :id, :user_id, CAST(:provider AS provider), :external_id, :secret, FALSE,
            '{"is_email": true}'::jsonb
        );
    """
    op.execute(
        sa.text(identity_sql).bindparams(
            id=uuid.uuid4(),
            user_id=user_id,
            provider="PASSWORD",
            external_id="dummy@user.com",
            secret=hashed_password
        )
    )
    
    wallet_sql = """
        INSERT INTO wallets (
            user_id, currency, balance, locked
        ) VALUES (
            :user_id, :currency, :balance, :locked
        );
    """
    op.execute(
        sa.text(wallet_sql).bindparams(
            user_id=user_id,
            currency="USD",
            balance=Decimal('0'),
            locked=Decimal('0')
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove admin user
    admin_id = uuid.UUID('00000000-0000-0000-0000-000000000001')
    op.execute(
        sa.text("DELETE FROM identities WHERE user_id = :id"),
        {"id": admin_id}
    )
    op.execute(
        sa.text("DELETE FROM users WHERE id = :id"),
        {"id": admin_id}
    )
