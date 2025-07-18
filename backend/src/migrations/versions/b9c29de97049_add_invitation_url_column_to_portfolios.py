"""add invitation_url column to portfolios

Revision ID: b9c29de97049
Revises: fb257d1590aa
Create Date: 2025-06-04 15:16:52.662627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9c29de97049'
down_revision: Union[str, None] = 'fb257d1590aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('portfolio_snapshots', 'nav_price',
               existing_type=sa.NUMERIC(precision=24, scale=8),
               nullable=False)
    op.add_column('portfolios', sa.Column('invitation_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('portfolios', 'invitation_url')
    op.alter_column('portfolio_snapshots', 'nav_price',
               existing_type=sa.NUMERIC(precision=24, scale=8),
               nullable=True)
    # ### end Alembic commands ###
