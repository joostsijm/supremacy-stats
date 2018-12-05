"""price_add_buy_boolean

Revision ID: 93f7c141aa44
Revises: ebe5d3f7ecd9
Create Date: 2018-12-05 14:32:08.167368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93f7c141aa44'
down_revision = 'ebe5d3f7ecd9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_prices', sa.Column('buy', sa.Boolean(), server_default='f', nullable=True))


def downgrade():
    op.drop_column('sp_prices', 'buy')
