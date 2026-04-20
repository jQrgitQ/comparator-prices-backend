"""Add image_url to products

Revision ID: 005_add_product_image
Revises: 004_stores
Create Date: 2026-04-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_product_image'
down_revision = '004_stores'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('products', sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('products', 'image_url')