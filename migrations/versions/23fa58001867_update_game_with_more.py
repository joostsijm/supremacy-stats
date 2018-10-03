"""update_game_with_more

Revision ID: 23fa58001867
Revises: fd83baca822b
Create Date: 2018-10-03 13:05:18.001345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23fa58001867'
down_revision = 'fd83baca822b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_games', sa.Column('ai_level', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('country_selection', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('gold_round', sa.Boolean(), nullable=True))
    op.add_column('sp_games', sa.Column('ranked', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('research_days_offset', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('research_time_scale', sa.DECIMAL(precision=2, scale=1), nullable=True))
    op.add_column('sp_games', sa.Column('team_setting', sa.Integer(), nullable=True))
    op.add_column('sp_games', sa.Column('time_scale', sa.DECIMAL(precision=2, scale=1), nullable=True))
    op.add_column('sp_games', sa.Column('victory_points', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'victory_points')
    op.drop_column('sp_games', 'time_scale')
    op.drop_column('sp_games', 'team_setting')
    op.drop_column('sp_games', 'research_time_scale')
    op.drop_column('sp_games', 'research_days_offset')
    op.drop_column('sp_games', 'ranked')
    op.drop_column('sp_games', 'gold_round')
    op.drop_column('sp_games', 'country_selection')
    op.drop_column('sp_games', 'ai_level')
