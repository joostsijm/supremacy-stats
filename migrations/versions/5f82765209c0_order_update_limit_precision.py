"""order_update_limit_precision

Revision ID: 5f82765209c0
Revises: 26dc4ea6f186
Create Date: 2018-11-30 12:01:51.738633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f82765209c0'
down_revision = '26dc4ea6f186'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('sp_orders', 'limit', type_=sa.DECIMAL(precision=3, scale=1), existing_type=sa.DECIMAL(precision=2, scale=1), nullable=True)
    pass


def downgrade():
    op.alter_column('sp_orders', 'limit', type_=sa.DECIMAL(precision=2, scale=1), existing_type=sa.DECIMAL(precision=1, scale=1), nullable=True)
    pass
