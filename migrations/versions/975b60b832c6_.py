"""empty message

Revision ID: 975b60b832c6
Revises: 680aefa41fa4
Create Date: 2022-07-24 14:55:35.175470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '975b60b832c6'
down_revision = '680aefa41fa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'seeking_description')
    # ### end Alembic commands ###
