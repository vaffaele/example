"""empty message

Revision ID: 25ca8afb4f10
Revises: 
Create Date: 2020-05-10 21:40:55.406943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25ca8afb4f10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('image_link', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('image_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'image_link')
    op.drop_column('actors', 'image_link')
    # ### end Alembic commands ###
