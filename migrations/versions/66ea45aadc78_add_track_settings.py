"""add_track_settings

Revision ID: 66ea45aadc78
Revises: cd7a9bbfdc80
Create Date: 2018-11-18 12:18:07.593895

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '66ea45aadc78'
down_revision = 'cd7a9bbfdc80'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_games', sa.Column('track_coalitions', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('track_game', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('track_market', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('track_players', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('track_relations', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('track_score', sa.Boolean(), nullable=True))
    op.drop_column('sp_games', 'fetch_at')
    op.drop_column('sp_games', 'last_result_time')


def downgrade():
    op.add_column('sp_games', sa.Column('last_result_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('sp_games', sa.Column('fetch_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('sp_games', 'track_score')
    op.drop_column('sp_games', 'track_relations')
    op.drop_column('sp_games', 'track_players')
    op.drop_column('sp_games', 'track_market')
    op.drop_column('sp_games', 'track_game')
    op.drop_column('sp_games', 'track_coalitions')
