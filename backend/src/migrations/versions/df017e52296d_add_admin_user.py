"""add admin user

Revision ID: df017e52296d
Revises: 34b6c15d6bd1
Create Date: 2025-06-16 01:55:44.962347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
import bcrypt
from datetime import datetime, UTC


# revision identifiers, used by Alembic.
revision: str = 'df017e52296d'
down_revision: Union[str, None] = '34b6c15d6bd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add admin user
    admin_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
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
            id=admin_id,
            secure_code="supersecret",
            display_name="Administrator",
            first_name="Admin",
            last_name="User",
            avatar_url=None,
            role="ADMIN",
        )
    )
    # Add credentials identity for admin user
    hashed_password = bcrypt.hashpw(b'adminpassword', bcrypt.gensalt()).decode()
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
            user_id=admin_id,
            provider="PASSWORD",
            external_id="admin@example.com",
            secret=hashed_password,
            # last_login_at=datetime.now(UTC)
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove admin user
    admin_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    op.execute(
        sa.text("DELETE FROM identities WHERE user_id = :id"),
        {"id": admin_id}
    )
    op.execute(
        sa.text("DELETE FROM users WHERE id = :id"),
        {"id": admin_id}
    )
