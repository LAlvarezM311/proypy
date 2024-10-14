from app import db
from app.models.shop import Shop

class Product(db.Model):
    """
    Modelo que representa un producto en el sistema.

    Cada producto tiene un nombre de producto, imagen de referencia, una breve descripción, un precio, una cantidad (unidades disponibles) y está asociado con una Tienda a través de una clave foránea.

    Atributos:
        id (int): Identificador único del producto (clave primaria).
        name (str): Nombre del producto, no puede ser nulo.
        image (str): Imagen de referencia del producto, no puede ser nulo.
        description (str): Descripción del producto, opcional.
        price (int): Precio del producto, no puede ser nulo.
        quantity (int): Cantidad en existencia del producto, no puede ser nulo.
        shop_id (int): Clave foránea que referencia la tienda a la cual pertenece el producto.
    """
    
    __tablename__ = 'Products'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    name = db.Column(db.String(100), nullable=False)  # Nombre del producto, no nulo
    image = db.Column(db.String(255), nullable=False)  # Imagen de referencia del producto, no nulo
    description = db.Column(db.String(255), nullable=True)  # Descripción del producto, opcional
    price = db.Column(db.Integer, nullable=False)  # Precio del producto, no nulo
    quantity = db.Column(db.Integer, nullable=False)  # Cantidad en existencia del producto, no nulo
    shop_id = db.Column(db.Integer, db.ForeignKey('Shops.id'), nullable=False)  # Clave foránea hacia la tabla 'Shop'

    # Relación con el modelo Shops
    shop = db.relationship('Shop', backref='Products')  # Define la relación con el modelo Shops y permite acceso inverso desde Shops a Products

    def __init__(self, name, image, description, price, quantity, shop_id):
        """
        Constructor de la clase Products.


        Args:
            name (str): El nombre del producto.
            image (str): Imagen de referencia del producto
            description (str): Descripción del producto.
            price (int): Precio del producto.
            quantity (int): Cantidad en existencia del producto.
            shop_id (int): El ID de la tienda asociada.
        """
        self.name = name
        self.image = image
        self.description = description
        self.price = price
        self.quantity = quantity
        self.shop_id = shop_id
