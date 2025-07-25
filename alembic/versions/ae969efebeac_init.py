"""init

Revision ID: ae969efebeac
Revises: ed62f4c6fc01
Create Date: 2025-07-17 10:22:19.650284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae969efebeac'
down_revision: Union[str, Sequence[str], None] = 'ed62f4c6fc01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'site', type_='foreignkey')
    op.drop_column('site', 'online')
    op.drop_column('site', 'link')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('link', sa.VARCHAR(), nullable=True))
    op.add_column('site', sa.Column('online', sa.BOOLEAN(), nullable=True))
    op.create_foreign_key(None, 'site', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###
