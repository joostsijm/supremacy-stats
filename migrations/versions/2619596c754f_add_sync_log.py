"""add_sync_log

Revision ID: 2619596c754f
Revises: 66ea45aadc78
Create Date: 2018-11-20 18:55:09.049814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2619596c754f'
down_revision = '66ea45aadc78'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sp_sync_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('function', sa.String(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('succes', sa.Boolean(), server_default='f', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sp_sync_log')
