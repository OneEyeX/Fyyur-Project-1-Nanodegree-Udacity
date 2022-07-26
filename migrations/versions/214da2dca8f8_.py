"""empty message

Revision ID: 214da2dca8f8
Revises: 975b60b832c6
Create Date: 2022-07-25 12:29:46.818323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214da2dca8f8'
down_revision = '975b60b832c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
