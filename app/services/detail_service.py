from app import db
from app.models.sale import Sale
from app.models.product import Product
from app.models.detail import SaleDetail

class SaleDetailService:
    """Servicio para manejar las operaciones CRUD y lógicas de los detalles de ventas."""

    @staticmethod
    def create_detail(qnt_prod_sale, sale_id, product_id):
        """Crear un nuevo detalle de venta con productos asociados.
        
        Args:
            qnt_prod_sale (int): Cantidad de productos vendidos asociados a un ID producto
            product_id (int): ID de producto a asociar.
            sale_id (int): ID venta asociada al detalle de venta.
    
        Returns:
            Detail: Nuevo detalle de venta creado.

        Raises:
            ValueError: Si los productos o las ventas especificados no existen.
        """
        # Buscar el producto asociado al Detalle por su ID
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            # Si no se encuentra el producto, lanzar una excepción
            raise ValueError('Product not found')

        # Buscar la venta asociada al Detalle por su ID
        sale = Sale.query.filter_by(id=sale_id).first()
        if not sale:
            # Si no se encuentra la venta, lanzar una excepción
            raise ValueError('Sale not found')

        # Crear una nueva instancia de Detail con el id de producto, cantidad de producto vendido, id de venta
        new_detail = SaleDetail(qnt_prod_sale=qnt_prod_sale, sale_id=sale.id, product_id=product.id)
        
        # Asociar los productos al detalle de venta
        new_detail.product = product
        
        # Asociar la Venta al detalle de venta
        new_detail.sale = sale

        # Agregar el nuevo detalle de venta a la sesión de base de datos
        db.session.add(new_detail)
        
        # Confirmar los cambios y guardar la nueva venta en la base de datos
        db.session.commit()
        
        return new_detail

    @staticmethod
    def update_detail(id, qnt_prod_sale=None, sale_id=None, product_id=None):
        """Actualizar los detalles de un detalle de venta existente o en proceso.
        
        Args:
            id (int): El ID del detalle de venta a actualizar.
            qnt_prod_sale (int): Cantidad de productos vendidos asociados a un ID producto
            product_id (int): ID de producto a asociar.
            sale_id (int): ID venta asociada al detalle de venta.

        Returns:
            Detail: El detalle de Venta actualizado.

        Raises:
            ValueError: Si el detalle de venta no se encuentra.
        """
        # Buscar el detalle de venta por su ID
        saledetail = SaleDetail.query.get(id)
        
        # Si el detalle de venta no existe, lanzar un error
        if not saledetail:
            raise ValueError('SaleDetail not found')
        
        # Si se proporcionó una nueva cantidad de producto, actualizarla
        if qnt_prod_sale:
            saledetail.qnt_prod_sale = qnt_prod_sale
    
        # Si se proporcionaron nuevos productos, actualizarlos
        if product_id:
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                raise ValueError('Product not found')
            saledetail.product_id = product.id

        # Si se proporcionaron nuevas ventas, actualizarlas
        if sale_id:
            sale = Sale.query.filter_by(id=sale_id).first()
            if not sale:
                raise ValueError('Sale not found')
            saledetail.sale_id = sale.id

        # Confirmar los cambios y actualizar el detalle de venta en la base de datos
        db.session.commit()
        
        return saledetail

    @staticmethod
    def delete_detail(id):
        """Eliminar un detalle de venta existente.
        
        Args:
            detail_id (int): El ID del detalle de venta a eliminar.

        Raises:
            ValueError: Si el detalle de venta no se encuentra.
        """
        # Buscar el detalle de venta por su ID
        saledetail = SaleDetail.query.get(id)
        
        # Si el detalle de venta no existe, lanzar un error
        if not saledetail:
            raise ValueError('SaleDetail not found')
        
        # Eliminar el detalle de Venta de la base de datos
        db.session.delete(saledetail)
        
        # Confirmar los cambios
        db.session.commit()

    @staticmethod
    def get_all_saledetails():
        """Obtener todos los detalles de ventas existentes.
        
        Returns:
            List[Details]: Lista de todos los detalles de ventas en la base de datos.
        """
        # Devolver todos los detalles de ventas almacenados
        return SaleDetail.query.all()

