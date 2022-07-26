"""empty message

Revision ID: 2551f51f1c55
Revises: 2f616878ed4d
Create Date: 2022-07-23 03:23:58.893628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2551f51f1c55'
down_revision = '2f616878ed4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('city', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('state', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('phone', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('image_link', sa.String(length=500), nullable=True))
    op.add_column('venues', sa.Column('facebook_link', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('description', sa.String(length=500), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'genres')
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'description')
    op.drop_column('venues', 'facebook_link')
    op.drop_column('venues', 'image_link')
    op.drop_column('venues', 'phone')
    op.drop_column('venues', 'address')
    op.drop_column('venues', 'state')
    op.drop_column('venues', 'city')
    # ### end Alembic commands ###
