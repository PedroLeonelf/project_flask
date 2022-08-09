"""empty message

Revision ID: 0281d61d9bde
Revises: 0c5762161baa
Create Date: 2022-08-08 00:38:53.064506

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0281d61d9bde'
down_revision = '0c5762161baa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'remember_me_token_created_at')
    op.drop_column('users', 'remember_me_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('remember_me_token', mysql.VARCHAR(length=80), nullable=True))
    op.add_column('users', sa.Column('remember_me_token_created_at', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
