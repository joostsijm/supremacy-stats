"""add_market_and_resource

Revision ID: 26dc4ea6f186
Revises: 22e4d4122e89
Create Date: 2018-11-28 13:56:19.722359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26dc4ea6f186'
down_revision = '22e4d4122e89'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sp_resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sp_market',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['sp_games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sp_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('limit', sa.DECIMAL(precision=2, scale=1), nullable=True),
    sa.Column('buy', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('market_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['market_id'], ['sp_market.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['sp_players.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['sp_resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sp_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.DECIMAL(precision=2, scale=1), nullable=True),
    sa.Column('market_id', sa.Integer(), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['market_id'], ['sp_market.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['sp_resource.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sp_prices')
    op.drop_table('sp_orders')
    op.drop_table('sp_market')
    op.drop_table('sp_resource')
