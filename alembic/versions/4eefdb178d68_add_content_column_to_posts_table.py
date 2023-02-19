"""add content column to posts table

Revision ID: 4eefdb178d68
Revises: 01069c1a4854
Create Date: 2023-02-19 18:30:17.123224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eefdb178d68'
down_revision = '01069c1a4854'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(50), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'Content')
    pass
