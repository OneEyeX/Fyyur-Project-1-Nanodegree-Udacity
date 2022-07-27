"""empty message

Revision ID: 54d3511ee37f
Revises: 922efdbf1e93
Create Date: 2022-07-27 09:59:45.872520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d3511ee37f'
down_revision = '922efdbf1e93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'link')
    # ### end Alembic commands ###