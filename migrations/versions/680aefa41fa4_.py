"""empty message

Revision ID: 680aefa41fa4
Revises: 3087ad967b5c
Create Date: 2022-07-24 14:55:18.806487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '680aefa41fa4'
down_revision = '3087ad967b5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
