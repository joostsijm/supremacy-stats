"""add_day_of_game

Revision ID: a9f27443ec47
Revises: 1fbaa8acee0f
Create Date: 2018-10-04 15:20:28.697138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9f27443ec47'
down_revision = '1fbaa8acee0f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_games', sa.Column('day_of_game', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'day_of_game')
