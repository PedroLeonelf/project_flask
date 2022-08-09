"""empty message

Revision ID: c1152fe1a905
Revises: 855b3bfd9067
Create Date: 2022-08-08 22:30:58.391244

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c1152fe1a905'
down_revision = '855b3bfd9067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'background',
               existing_type=mysql.ENUM('#FFF001', '#FEC10E', '#F7921E', '#EF6421', '#EB1C24', '#932490', '#000000', '#642C91', '#0070BA', '#01ABEF', '#01A99C', '#01A451', '#8BC53D', '#C4C4C4'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'background',
               existing_type=mysql.ENUM('#FFF001', '#FEC10E', '#F7921E', '#EF6421', '#EB1C24', '#932490', '#000000', '#642C91', '#0070BA', '#01ABEF', '#01A99C', '#01A451', '#8BC53D', '#C4C4C4'),
               nullable=False)
    # ### end Alembic commands ###
