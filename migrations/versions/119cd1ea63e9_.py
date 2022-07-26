"""empty message

Revision ID: 119cd1ea63e9
Revises: c996c35fe067
Create Date: 2022-07-24 09:30:29.251764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '119cd1ea63e9'
down_revision = 'c996c35fe067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('venues', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('venues', 'seeking_description')
    # ### end Alembic commands ###
