"""price_update_value_precision

Revision ID: ebe5d3f7ecd9
Revises: 5f82765209c0
Create Date: 2018-11-30 12:17:24.742366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe5d3f7ecd9'
down_revision = '5f82765209c0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('sp_prices', 'value', type_=sa.DECIMAL(precision=3, scale=1), existing_type=sa.DECIMAL(precision=2, scale=1), nullable=True)
    pass


def downgrade():
    op.alter_column('sp_prices', 'value', type_=sa.DECIMAL(precision=2, scale=1), existing_type=sa.DECIMAL(precision=3, scale=1), nullable=True)
    pass
