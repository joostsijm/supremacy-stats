"""fix_next_day_datatype

Revision ID: 897faef2f09d
Revises: d3a3eafe1aa3
Create Date: 2018-10-03 18:03:19.572422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '897faef2f09d'
down_revision = 'd3a3eafe1aa3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('sp_games', 'next_day_time')
    op.add_column('sp_games', sa.Column('next_day_time', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('sp_games', 'next_day_time')
    op.add_column('sp_games', sa.Column('next_day_time', sa.Integer(), nullable=True))
