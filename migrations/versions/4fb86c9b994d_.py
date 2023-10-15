"""empty message

Revision ID: 4fb86c9b994d
Revises: 974a01b4444a
Create Date: 2023-10-15 03:43:37.201258

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4fb86c9b994d'
down_revision = '974a01b4444a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('work_place', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_password_hash'), ['password_hash'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_phone_number'), ['phone_number'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_work_place'), ['work_place'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_year'), ['year'], unique=False)

    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.drop_index('ix_restaurant_address')
        batch_op.drop_index('ix_restaurant_avg_price')
        batch_op.drop_index('ix_restaurant_location')
        batch_op.drop_index('ix_restaurant_name')
        batch_op.drop_index('ix_restaurant_ratings')

    op.drop_table('restaurant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ratings', mysql.FLOAT(), nullable=True),
    sa.Column('location', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('address', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('avg_price', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.create_index('ix_restaurant_ratings', ['ratings'], unique=False)
        batch_op.create_index('ix_restaurant_name', ['name'], unique=False)
        batch_op.create_index('ix_restaurant_location', ['location'], unique=False)
        batch_op.create_index('ix_restaurant_avg_price', ['avg_price'], unique=False)
        batch_op.create_index('ix_restaurant_address', ['address'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_year'))
        batch_op.drop_index(batch_op.f('ix_user_work_place'))
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_role'))
        batch_op.drop_index(batch_op.f('ix_user_phone_number'))
        batch_op.drop_index(batch_op.f('ix_user_password_hash'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
