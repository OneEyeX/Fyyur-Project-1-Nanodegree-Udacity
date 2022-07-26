"""empty message

Revision ID: 9e25f845128c
Revises: 62c8873197e8
Create Date: 2022-07-23 03:15:40.757296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9e25f845128c'
down_revision = '62c8873197e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'facebook_link')
    op.drop_column('venues', 'phone')
    op.drop_column('venues', 'genres')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'image_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('venues', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###