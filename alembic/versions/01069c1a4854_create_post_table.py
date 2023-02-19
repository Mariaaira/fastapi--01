"""create post table

Revision ID: 01069c1a4854
Revises: 
Create Date: 2023-02-19 16:58:09.421902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01069c1a4854'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String(50), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
