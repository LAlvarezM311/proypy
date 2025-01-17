"""Initial migration.

Revision ID: d27749f076a8
Revises: 
Create Date: 2024-10-16 18:49:54.356020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd27749f076a8'
down_revision = None
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Detalle_Venta')
    op.drop_table('Products')
    op.drop_table('Ventas')
    op.drop_table('Shops')
    # ### end Alembic commands ###
