from app import db
from app.models.sale import Sale, StateEnum
from app.models.product import Product
import enum

class SaleService:
    """Servicio para manejar las operaciones CRUD y lógicas de las ventas."""

    @staticmethod
    def create_sale(date, total, status):
        """Crear una nueva venta con productos asociados.
        
        Args:
            date (date): Fecha de la venta.
            total (int): Valor total de la venta.
            status (enum): Estado de la transacción.
            

        Returns:
            Sale: La nueva venta creada.

        Raises:
            ValueError: Si los productos especificados no existen.
        """

        
        # Crear una nueva instancia de Sale 
        new_sale = Sale(date=date, total=total, status=StateEnum(status))
        
        
        # Agregar la nueva venta a la sesión de base de datos
        db.session.add(new_sale)
        
        # Confirmar los cambios y guardar la nueva venta en la base de datos
        db.session.commit()
        
        return new_sale

    @staticmethod
    def update_sale(sale_id, date=None, total=None, status=None):
        """Actualizar los detalles de una venta existente o en proceso.
        
        Args:
            sale_id (int): El ID de la venta a actualizar.
            date (date): Fecha de la venta.
            total (int): Valor total de la venta.
            status (enum): Estado de la transacción.
            

        Returns:
            Sale: La Venta actualizada.

        Raises:
            ValueError: Si la venta no se encuentra.
        """
        # Buscar la venta por su ID
        sale = Sale.query.get(sale_id)
        
        # Si la venta no existe, lanzar un error
        if not sale:
            raise ValueError('Sale not found')
        
        # Si se proporcionó una nueva fecha, actualizarla
        if date:
            sale.date = date
        
        # Si se proporcionó un nuevo total, actualizarlo
        if total:
            sale.total = total
        
        # Si se proporcionó un nuevo estado de Venta, actualizarlo
        if status is not None:
            sale.status = StateEnum(status)      
       
        # Confirmar los cambios y actualizar la venta en la base de datos
        db.session.commit()
        
        return sale

    @staticmethod
    def delete_sale(sale_id):
        """Eliminar una venta existente.
        
        Args:
            sale_id (int): El ID de la venta a eliminar.

        Raises:
            ValueError: Si la venta no se encuentra.
        """
        # Buscar la venta por su ID
        sale = Sale.query.get(sale_id)
        
        # Si la Venta no existe, lanzar un error
        if not sale:
            raise ValueError('Sale not found')
        
        # Eliminar la Venta de la base de datos
        db.session.delete(sale)
        
        # Confirmar los cambios
        db.session.commit()

    @staticmethod
    def get_all_sales():
        """Obtener todas las ventas existentes.
        
        Returns:
            List[Sales]: Lista de todas las ventas en la base de datos.
        """
        # Devolver todas las ventas almacenadas
        return Sale.query.all()

    @staticmethod
    def mark_sale_paid(sale_id):
        """Marcar una venta como pagada.
        
        Args:
            sale_id (int): El ID de la venta a marcar como pagada.

        Returns:
            Sale: La venta con el estado actualizado.

        Raises:
            ValueError: Si la venta no se encuentra.
        """
        # Buscar la venta por su ID
        sale = Sale.query.get(sale_id)
        
        # Si la Venta no existe, lanzar un error
        if not sale:
            raise ValueError('Sale not found')
        
        # Marcar la Venta como pagada
        sale.status = StateEnum.PAID
        
        # Confirmar los cambios
        db.session.commit()
        
        return sale

    @staticmethod
    def mark_sale_inprogress(sale_id):
        """Marcar una venta en proceso.
        
        Args:
            sale_id (int): El ID de la venta a marcar en proceso.

        Returns:
            Sale: La venta con el estado actualizado.

        Raises:
            ValueError: Si la venta no se encuentra.
        """
        # Buscar la venta por su ID
        sale = Sale.query.get(sale_id)
        
        # Si la Venta no existe, lanzar un error
        if not sale:
            raise ValueError('Sale not found')
                
        # Marcar la venta en proceso
        sale.status = StateEnum.IN_PROGRESS
        
        # Confirmar los cambios
        db.session.commit()
        
        return sale
