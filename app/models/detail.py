from app import db
from app.models.sale import Sale
from app.models.product import Product

# Tabla intermedia para la relación de muchos a muchos entre Ventas y Productos
class SaleDetail(db.Model):
    __tablename__='Detalle_Venta'

    # Columnas no foráneas
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    qnt_prod_sale = db.Column(db.Integer, nullable=False)  # Cantidad vendida de un producto, no nulo

    # Columnas foráneas
    sale_id = db.Column(db.Integer, db.ForeignKey('Ventas.id'), primary_key=True)  # Referencia a la tabla 'sale'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)  # Referencia a la tabla 'product'

    # Relación muchos a muchos con productos usando la tabla intermedia 'sale_detail'
    product = db.relationship('Product', backref=db.backref('Detalle_Venta', lazy=True))  # Permite acceso inverso desde ventas a productos
    sale = db.relationship('Sale', backref=db.backref('Detalle_Venta', lazy=True))  # Permite acceso inverso desde ventas a productos


    def __init__(self, qnt_prod_sale, sale_id, product_id):
        """
        Constructor de la clase SaleDetail.
        
        Args:
            qnt_prod_sale (int): Cantidad de producto vendido.

        """
        self.qnt_prod_sale = qnt_prod_sale
        self.sale_id = sale_id
        self.product_id = product_id
