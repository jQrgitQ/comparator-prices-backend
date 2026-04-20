"""Create categories and subcategories

Revision ID: 003_categories_subcategories
Revises: 002_products_prices
Create Date: 2026-04-18 16:30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '003_categories_subcategories'
down_revision: Union[str, None] = '002_products_prices'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)

    op.create_table(
        'subcategories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subcategories_id'), 'subcategories', ['id'], unique=False)
    op.create_index(op.f('ix_subcategories_name'), 'subcategories', ['name'], unique=False)

    op.create_index(op.f('ix_subcategories_category_id'), 'subcategories', ['category_id'], unique=False)

    op.add_column('products', sa.Column('subcategory_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_products_subcategory_id', 'products', 'subcategories', ['subcategory_id'], ['id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_products_subcategory_id'), table_name='products')
    op.drop_column('products', 'subcategory_id')
    op.drop_index(op.f('ix_subcategories_category_id'), table_name='subcategories')
    op.drop_index(op.f('ix_subcategories_name'), table_name='subcategories')
    op.drop_index(op.f('ix_subcategories_id'), table_name='subcategories')
    op.drop_table('subcategories')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')