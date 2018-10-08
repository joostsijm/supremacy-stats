"""user_add_image_id

Revision ID: cd7a9bbfdc80
Revises: a9f27443ec47
Create Date: 2018-10-08 16:15:08.222628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cd7a9bbfdc80'
down_revision = 'a9f27443ec47'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_players', sa.Column('flag_image_id', sa.Integer(), nullable=True))
    op.add_column('sp_players', sa.Column('player_image_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('sp_players', 'player_image_id')
    op.drop_column('sp_players', 'flag_image_id')
