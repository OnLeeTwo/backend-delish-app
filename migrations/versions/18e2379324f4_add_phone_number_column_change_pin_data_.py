"""add phone_number column & change pin data type

Revision ID: 18e2379324f4
Revises: fe1c402a1179
Create Date: 2024-11-14 12:46:45.552553

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '18e2379324f4'
down_revision = 'fe1c402a1179'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('pin',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=8),
               existing_nullable=False)

    with op.batch_alter_table('user_information', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(length=255), nullable=False))
        batch_op.create_unique_constraint(None, ['phone_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_information', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('phone_number')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('pin',
               existing_type=sa.String(length=8),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###