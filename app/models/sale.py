from app import db
import enum

class StateEnum(enum.Enum):
    IN_PROGRESS=0
    REGISTERED=1
    PAID=2
    NULLED=3


class Sale(db.Model):
    """
    Modelo que representa una venta en el sistema.

    Cada venta puede contener varios productos, estos productos están contenidos en una o varias tiendas.

    Atributos:
        id (int): Identificador único de la venta (clave primaria).
        date (date): Fecha de la venta, no nulo.
        total (int): Valor total de la venta, no nulo.
        status (enum): Estado de la transacción.
        products (list): Relación muchos a muchos con la tabla de productos.
    """
    
    __tablename__ = 'Ventas'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    date = db.Column(db.Date, nullable=False)  # Fecha de la venta, no puede ser nulo
    total = db.Column(db.Integer, nullable=False) # Valor total de la venta, no puede ser nulo (en caso de ser anulada el valor es cero)
    status = db.Column(db.Enum(StateEnum), nullable=False) # Estado de la Transacción con las opciones: en proceso, registrado, pagado

    # Relación muchos a muchos con productos usando la tabla intermedia 'sale_detail'
    # product = db.relationship('Product', back_populates='Detalle_Venta')  # Permite acceso inverso desde ventas a productos
    # sale = db.relationship('Sale', back_populates='Detalle_Venta')  # Permite acceso inverso desde ventas a productos

    def __init__(self, date, total, status):
        """
        Constructor de la clase Sale.
        
        Args:
            date (date): Fecha de la venta.
            total (int): Valor total de la venta.
            status (enum): Estado de la transacción.
        """
        self.date = date
        self.total = total
        self.status = status
