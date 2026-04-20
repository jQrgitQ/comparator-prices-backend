"""Create products and prices tables

Revision ID: 002_products_prices
Revises: 001_initial_auth
Create Date: 2026-04-18 16:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002_products_prices'
down_revision: Union[str, None] = '001_initial_auth'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)

    op.create_table(
        'prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('discount_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('is_discount', sa.Boolean(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prices_id'), 'prices', ['id'], unique=False)
    op.create_index(op.f('ix_prices_date'), 'prices', ['date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_prices_date'), table_name='prices')
    op.drop_index(op.f('ix_prices_id'), table_name='prices')
    op.drop_table('prices')
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')