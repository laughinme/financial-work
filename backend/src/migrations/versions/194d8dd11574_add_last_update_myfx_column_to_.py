"""add "last_update_myfx" column to portfolios

Revision ID: 194d8dd11574
Revises: ffbbeaf58c89
Create Date: 2025-06-05 18:27:39.806811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '194d8dd11574'
down_revision: Union[str, None] = 'ffbbeaf58c89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('portfolios', sa.Column('last_update_myfx', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('portfolios', 'last_update_myfx')
    # ### end Alembic commands ###
