from app import db

class Shop(db.Model): # Se crea modelo de la tabla Tiendas
    """
    Modelo que representa una Tienda en el sistema.

    Cada Tienda tiene asociado varios productos los cuales ofrece para venta en la App.

    Atributos:
        id (int): Identificador único de la tienda (clave primaria).
        name (str): Nombre de la Tienda, debe ser único y no nulo.
        logo (str): Logo de la Tienda, debe ser único y no nulo.
        description (str): Descripción de la Tienda, es opcional.
        phone (str): Teléfono de contacto de la Tienda, debe ser único y no nulo.
        address (str): Dirección de la Tienda, debe ser único y no nulo.
        email (str): Correo electrónico de la Tienda, debe ser único y no nulo.
    """
    
    __tablename__ = 'Shops'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    name = db.Column(db.String(100), unique=True, nullable=False)  # Nombre de la Tienda, debe ser único y no nulo
    logo = db.Column(db.String(255), unique=True, nullable=False)  # Logo de la Tienda, debe ser único y no nulo
    description = db.Column(db.String(255), nullable=True)  # Descripción de la Tienda, es opcional
    phone = db.Column(db.String(12), unique=True, nullable=False)  # Teléfono de la Tienda, debe ser único y no nulo
    address = db.Column(db.String(100), unique=True, nullable=False)  # Dirección de la Tienda, debe ser único y no nulo
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email de la Tienda, debe ser único y no nulo

    def __init__(self, name, logo, description, phone, address, email):

        """
        Constructor de la clase Shop.

        Args:
            name (str): El nombre de la tienda.
            logo (str): Logo de la tienda.
            description (str): Descripción de la tienda.
            phone (str): El teléfono de contacto de la tienda.
            address (str): La dirección de la tienda.
            email (str): El correo electrónico de la tienda.
        """

        self.name = name
        self.logo = logo
        self.description = description
        self.phone = phone
        self.address = address
        self.email = email
