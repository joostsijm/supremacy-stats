"""unique_email

Revision ID: 638f01077627
Revises: 47e4599484a1
Create Date: 2018-05-11 10:04:21.416693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '638f01077627'
down_revision = '47e4599484a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'sp_users', ['email'])


def downgrade():
    op.drop_constraint(None, 'sp_users', type_='unique')
