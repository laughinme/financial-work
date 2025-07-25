"""expand drawdown possible rounding

Revision ID: 59272f79ed08
Revises: 26a5c9e32115
Create Date: 2025-06-17 18:38:28.947747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59272f79ed08'
down_revision: Union[str, None] = '26a5c9e32115'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('portfolio_snapshots', 'drawdown',
               existing_type=sa.NUMERIC(precision=6, scale=3),
               type_=sa.DECIMAL(precision=7, scale=3),
               existing_nullable=False)
    op.alter_column('portfolios', 'drawdown',
               existing_type=sa.NUMERIC(precision=6, scale=3),
               type_=sa.DECIMAL(precision=7, scale=3),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('portfolios', 'drawdown',
               existing_type=sa.DECIMAL(precision=7, scale=3),
               type_=sa.NUMERIC(precision=6, scale=3),
               existing_nullable=False)
    op.alter_column('portfolio_snapshots', 'drawdown',
               existing_type=sa.DECIMAL(precision=7, scale=3),
               type_=sa.NUMERIC(precision=6, scale=3),
               existing_nullable=False)
    # ### end Alembic commands ###
