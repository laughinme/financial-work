"""Add admin user

Revision ID: 2bd88bf14230
Revises: fbb5307d28a7
Create Date: 2025-06-13 23:21:28.408183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
import bcrypt


# revision identifiers, used by Alembic.
revision: str = '2bd88bf14230'
down_revision: Union[str, None] = 'fbb5307d28a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add admin user
    admin_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    user_insert_sql = """
        INSERT INTO users (
            id, secure_code, display_name, first_name, last_name, avatar_url, role
        ) VALUES (
            :id, :secure_code, :display_name, :first_name, :last_name, :avatar_url,
            CAST(:role AS role)
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
    # Add credentials for admin user
    hashed_password = bcrypt.hashpw(b'adminpassword', bcrypt.gensalt()).decode()
    creds_sql = """
        WITH new_auth AS (
            INSERT INTO auth_providers (user_id, provider, provider_user_id)
            VALUES (:user_id, CAST(:provider AS provider), :provider_user_id)
            RETURNING id
        )
        INSERT INTO credentials_providers (id, is_email, password, is_verified)
        SELECT id, TRUE, :password, FALSE FROM new_auth;
    """
    op.execute(
        sa.text(creds_sql).bindparams(
            user_id=admin_id,
            provider="CREDENTIALS",
            provider_user_id="admin@example.com",
            password=hashed_password,
        )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Remove admin user
    admin_id = uuid.UUID('11111111-1111-1111-1111-111111111111')
    op.execute(
        sa.text("DELETE FROM users WHERE id = :id"),
        {"id": admin_id}
    )
    # ### end Alembic commands ###
