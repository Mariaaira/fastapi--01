"""add content column to posts table

Revision ID: 5f8fa0598207
Revises: 4eefdb178d68
Create Date: 2023-02-19 18:38:54.420084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f8fa0598207'
down_revision = '4eefdb178d68'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(50), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
