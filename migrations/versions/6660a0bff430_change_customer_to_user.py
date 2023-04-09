"""change  customer to user

Revision ID: 6660a0bff430
Revises: 8fa18a42f794
Create Date: 2023-04-09 11:43:53.780403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6660a0bff430'
down_revision = '8fa18a42f794'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.CHAR(36), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=1000), nullable=False),
    sa.Column('given_name', sa.String(length=100), nullable=True),
    sa.Column('family_name', sa.String(length=100), nullable=True),
    sa.Column('patronymic', sa.String(length=100), nullable=True),
    sa.Column('phone_number', sa.String(length=11), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('home', sa.String(length=100), nullable=True),
    sa.Column('flat', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('customers')
    op.add_column('orders', sa.Column('user', sa.CHAR(36), nullable=True))
    op.alter_column('orders', 'order_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('orders', 'price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('fk_orders_customers_id_customer', 'orders', type_='foreignkey')
    op.create_foreign_key('fk_orders_users_id_user', 'orders', 'users', ['user'], ['id'])
    op.drop_column('orders', 'customer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('customer', sa.CHAR(length=36), nullable=True))
    op.drop_constraint('fk_orders_users_id_user', 'orders', type_='foreignkey')
    op.create_foreign_key('fk_orders_customers_id_customer', 'orders', 'customers', ['customer'], ['id'])
    op.alter_column('orders', 'price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('orders', 'order_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.drop_column('orders', 'user')
    op.create_table('customers',
    sa.Column('id', sa.CHAR(length=36), nullable=False),
    sa.Column('given_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('family_name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('patronymic', sa.VARCHAR(length=100), nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=11), nullable=False),
    sa.Column('city', sa.VARCHAR(length=100), nullable=False),
    sa.Column('street', sa.VARCHAR(length=100), nullable=False),
    sa.Column('home', sa.VARCHAR(length=100), nullable=False),
    sa.Column('flat', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
