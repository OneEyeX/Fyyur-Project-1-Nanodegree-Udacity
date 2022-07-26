"""empty message

Revision ID: 3087ad967b5c
Revises: 119cd1ea63e9
Create Date: 2022-07-24 12:20:50.543477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3087ad967b5c'
down_revision = '119cd1ea63e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('available', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'available')
    # ### end Alembic commands ###
