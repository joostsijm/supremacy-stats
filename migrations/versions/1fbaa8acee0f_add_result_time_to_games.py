"""add_result_time_to_games

Revision ID: 1fbaa8acee0f
Revises: 897faef2f09d
Create Date: 2018-10-04 15:04:27.652519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fbaa8acee0f'
down_revision = '897faef2f09d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_games', sa.Column('last_result_time', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'last_result_time')
