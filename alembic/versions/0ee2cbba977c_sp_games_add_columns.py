"""sp_games add columns

Revision ID: 0ee2cbba977c
Revises: c786de9727ed
Create Date: 2018-03-13 14:29:01.149551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ee2cbba977c'
down_revision = 'c786de9727ed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_games', sa.Column('fetch_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'fetch_at')
