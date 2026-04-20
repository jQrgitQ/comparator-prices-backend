"""Create stores table

Revision ID: 004_stores
Revises: 003_categories_subcategories
Create Date: 2026-04-18 17:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '004_stores'
down_revision: Union[str, None] = '003_categories_subcategories'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('location', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stores_id'), 'stores', ['id'], unique=False)
    op.create_index(op.f('ix_stores_name'), 'stores', ['name'], unique=False)

    op.add_column('prices', sa.Column('store_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_prices_store_id', 'prices', 'stores', ['store_id'], ['id'])


def downgrade() -> None:
    op.drop_foreign_key('fk_prices_store_id', 'prices')
    op.drop_column('prices', 'store_id')
    op.drop_index(op.f('ix_stores_name'), table_name='stores')
    op.drop_index(op.f('ix_stores_id'), table_name='stores')
    op.drop_table('stores')