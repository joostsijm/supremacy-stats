"""update_game

Revision ID: fd83baca822b
Revises: 638f01077627
Create Date: 2018-10-03 12:36:22.324062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd83baca822b'
down_revision = '638f01077627'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_coalitions', sa.Column('end_day', sa.Integer(), nullable=True))
    op.add_column('sp_coalitions', sa.Column('start_day', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('end_of_game', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('number_of_players', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('password', sa.String(), nullable=True))
    op.add_column('sp_games', sa.Column('scenario', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'scenario')
    op.drop_column('sp_games', 'password')
    op.drop_column('sp_games', 'number_of_players')
    op.drop_column('sp_games', 'end_of_game')
    op.drop_column('sp_coalitions', 'start_day')
    op.drop_column('sp_coalitions', 'end_day')
