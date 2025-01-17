"""empty message

Revision ID: ed649ad4e7a4
Revises: d27749f076a8
Create Date: 2024-10-16 19:35:12.729949

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ed649ad4e7a4'
down_revision = 'd27749f076a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('logo', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('logo'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('Ventas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('IN_PROGRESS', 'REGISTERED', 'PAID', 'NULLED', name='stateenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['Shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Detalle_Venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qnt_prod_sale', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['Products.id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['Ventas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('ventas')
    op.drop_table('detalle_venta')
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.drop_index('address')
        batch_op.drop_index('email')
        batch_op.drop_index('logo')
        batch_op.drop_index('name')
        batch_op.drop_index('phone')

    op.drop_table('shops')
    op.drop_table('products')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('image', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('price', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('shop_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], name='products_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('shops',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('logo', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('phone', mysql.VARCHAR(length=12), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.create_index('phone', ['phone'], unique=True)
        batch_op.create_index('name', ['name'], unique=True)
        batch_op.create_index('logo', ['logo'], unique=True)
        batch_op.create_index('email', ['email'], unique=True)
        batch_op.create_index('address', ['address'], unique=True)

    op.create_table('detalle_venta',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('qnt_prod_sale', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sale_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='detalle_venta_ibfk_1'),
    sa.ForeignKeyConstraint(['sale_id'], ['ventas.id'], name='detalle_venta_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('ventas',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), nullable=False),
    sa.Column('total', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', mysql.ENUM('IN_PROGRESS', 'REGISTERED', 'PAID', 'NULLED'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Detalle_Venta')
    op.drop_table('Products')
    op.drop_table('Ventas')
    op.drop_table('Shops')
    # ### end Alembic commands ###
