"""price_add_previous

Revision ID: 3b758f861a35
Revises: 19a50e3fbc21
Create Date: 2018-12-14 12:04:02.902942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b758f861a35'
down_revision = '19a50e3fbc21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_prices', sa.Column('previous_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sp_prices', 'sp_prices', ['previous_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'sp_prices', type_='foreignkey')
    op.drop_column('sp_prices', 'previous_id')
