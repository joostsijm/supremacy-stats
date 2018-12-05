"""resource_add_color

Revision ID: 916f1db42449
Revises: 93f7c141aa44
Create Date: 2018-12-05 15:03:55.563402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '916f1db42449'
down_revision = '93f7c141aa44'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_resource', sa.Column('color', sa.String(), nullable=True))


def downgrade():
    op.drop_column('sp_resource', 'color')
