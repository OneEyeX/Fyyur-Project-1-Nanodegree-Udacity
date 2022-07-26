"""empty message

Revision ID: 62c8873197e8
Revises: 9fc8defb1310
Create Date: 2022-07-23 02:08:41.757235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62c8873197e8'
down_revision = '9fc8defb1310'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'shows', 'artists', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'shows', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'artist_id')
    op.drop_column('shows', 'venue_id')
    # ### end Alembic commands ###
