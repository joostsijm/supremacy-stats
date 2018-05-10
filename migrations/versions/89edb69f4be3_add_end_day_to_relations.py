"""add end day to relations

Revision ID: 89edb69f4be3
Revises: 60f7fce83f27
Create Date: 2018-05-06 11:52:18.075456

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '89edb69f4be3'
down_revision = '60f7fce83f27'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_relations', sa.Column('end_day', sa.Integer(), nullable=True))
    op.drop_column('sp_users', 'password')
    op.drop_column('sp_users', 'email')
    op.drop_column('sp_users', 'registration_at')


def downgrade():
    op.add_column('sp_users', sa.Column('registration_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('sp_users', sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('sp_users', sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('sp_relations', 'end_day')
