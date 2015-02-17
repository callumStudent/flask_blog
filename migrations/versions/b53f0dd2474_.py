"""empty message

Revision ID: b53f0dd2474
Revises: a4c6606d74f
Create Date: 2015-02-11 17:36:22.437515

"""

# revision identifiers, used by Alembic.
revision = 'b53f0dd2474'
down_revision = 'a4c6606d74f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('slug', sa.String(length=256), nullable=True))
    op.alter_column('post', 'live',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.create_unique_constraint(None, 'post', ['slug'])
    op.alter_column('user', 'is_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'is_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_constraint(None, 'post', type_='unique')
    op.alter_column('post', 'live',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('post', 'slug')
    ### end Alembic commands ###
