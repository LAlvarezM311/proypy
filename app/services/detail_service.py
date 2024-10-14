from app import db
from app.models.sale import Sale
from app.models.product import Product
from app.models.detail import SaleDetail

class SaleDetailService:
    """Servicio para manejar las operaciones CRUD y lógicas de los detalles de ventas."""

    @staticmethod
    def create_detail(qnt_prod_sale, product_id, sale_id):
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
        products = Product.query.filter_by(idp=product_id).first()
        if not products:
            # Si no se encuentra el producto, lanzar una excepción
            raise ValueError('Product not found')

        # Buscar la venta asociada al Detalle por su ID
        sales = Sale.query.filter_by(ids=sale_id).first()
        if not sales:
            # Si no se encuentra la venta, lanzar una excepción
            raise ValueError('Sale not found')

        # Crear una nueva instancia de Detail con el id de producto, cantidad de producto vendido, id de venta
        new_detail = SaleDetail(product_id=products.idp, qnt_prod_sale=qnt_prod_sale, sale_id=sales.ids)
        
        # Asociar los productos al detalle de venta
        new_detail.products = products
        
        # Asociar la Venta al detalle de venta
        new_detail.sales = sales

        # Agregar el nuevo detalle de venta a la sesión de base de datos
        db.session.add(new_detail)
        
        # Confirmar los cambios y guardar la nueva venta en la base de datos
        db.session.commit()
        
        return new_detail

    @staticmethod
    def update_sale(detail_id, qnt_prod_sale=None, sales_ids=None, products_ids=None):
        """Actualizar los detalles de un detalle de venta existente o en proceso.
        
        Args:
            detail_id (int): El ID del detalle de venta a actualizar.
            qnt_prod_sale (int): Cantidad de productos vendidos asociados a un ID producto
            products_ids (int): ID de producto a asociar.
            sales_ids (int): ID venta asociada al detalle de venta.

        Returns:
            Detail: El detalle de Venta actualizado.

        Raises:
            ValueError: Si el detalle de venta no se encuentra.
        """
        # Buscar el detalle de venta por su ID
        saledetail = SaleDetail.query.get(detail_id)
        
        # Si el detalle de venta no existe, lanzar un error
        if not saledetail:
            raise ValueError('SaleDetail not found')
        
        # Si se proporcionó una nueva cantidad de producto, actualizarla
        if qnt_prod_sale:
            saledetail.qnt_prod_sale = qnt_prod_sale
    
        # Si se proporcionaron nuevos productos, actualizarlos
        if products_ids:
            products = Product.query.filter(Product.id.in_(products_ids)).all()
            saledetail.products = products

        # Si se proporcionaron nuevas ventas, actualizarlas
        if sales_ids:
            sales = Sale.query.filter(Sale.id.in_(sales_ids)).all()
            saledetail.sales = sales

        # Confirmar los cambios y actualizar el detalle de venta en la base de datos
        db.session.commit()
        
        return saledetail

    @staticmethod
    def delete_detail(detail_id):
        """Eliminar un detalle de venta existente.
        
        Args:
            detail_id (int): El ID del detalle de venta a eliminar.

        Raises:
            ValueError: Si el detalle de venta no se encuentra.
        """
        # Buscar el detalle de venta por su ID
        saledetail = SaleDetail.query.get(detail_id)
        
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

