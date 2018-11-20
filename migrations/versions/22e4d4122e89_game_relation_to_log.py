"""game_relation_to_log

Revision ID: 22e4d4122e89
Revises: 2619596c754f
Create Date: 2018-11-20 19:06:35.257788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22e4d4122e89'
down_revision = '2619596c754f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_sync_log', sa.Column('game_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sp_sync_log', 'sp_games', ['game_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'sp_sync_log', type_='foreignkey')
    op.drop_column('sp_sync_log', 'game_id')
