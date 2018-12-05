"""add_computer_settings_to_player

Revision ID: 9ed7859d34f7
Revises: 66ea45aadc78
Create Date: 2018-12-05 01:58:29.974100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed7859d34f7'
down_revision = '66ea45aadc78'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_players', sa.Column('computer_player', sa.Boolean(), server_default='f', nullable=True))
    op.add_column('sp_players', sa.Column('native_computer', sa.Boolean(), server_default='f', nullable=True))


def downgrade():
    op.drop_column('sp_players', 'native_computer')
    op.drop_column('sp_players', 'computer_player')
