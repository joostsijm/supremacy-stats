"""upgrade_user

Revision ID: 60f7fce83f27
Revises: 0ee2cbba977c
Create Date: 2018-04-24 08:47:48.958725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60f7fce83f27'
down_revision = '0ee2cbba977c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sp_users', sa.Column('email', sa.String(length=255), nullable=True))
    op.add_column('sp_users', sa.Column('password', sa.String(length=255), nullable=True))
    op.add_column('sp_users', sa.Column('registration_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('sp_users', 'registration_at')
    op.drop_column('sp_users', 'password')
    op.drop_column('sp_users', 'email')
