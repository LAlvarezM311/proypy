from app import db
from app.models.product import Product
from app.models.shop import Shop

class ProductService:
    @staticmethod
    def create_product(name, image, description, price, quantity, shop_id):
        """
        Crear un nuevo producto para una tienda específica.
        
        Args:
            name (str): Nombre del nuevo producto.
            image (str): Imagen de referencia del nuevo producto.
            description (str): Descripción del nuevo producto.
            price (int): Precio del nuevo producto.
            quantity (int): Cantidad en existencia del nuevo producto.
            shop_id (int): ID de la tienda a la cual pertenece el producto.
        
        Returns:
            Product: El producto creado.
        
        Raises:
            ValueError: Si la tienda no se encuentra.
        """
        # Buscar la tienda asociada al producto por su ID
        shop = Shop.query.filter_by(id=shop_id).first()
        if not shop:
            # Si no se encuentra la tienda, lanzar una excepción
            raise ValueError('Shop not found')

        
        # Crear un nuevo objeto Product para la tienda asociada
        product = Product(name=name, image=image, description=description, price=price, quantity=quantity, shop_id=shop.id)
        
        # Añadir el nuevo producto a la base de datos
        db.session.add(product)
        db.session.commit()
        
        return product  # Retornar el producto recién creado
    
    @staticmethod
    def get_all_products():
        """
        Obtener todos los productos de la base de datos.
        
        Returns:
            List[Product]: Lista de todos los productos en la base de datos.
        """
        # Recuperar todos los registros de la tabla Product
        return Product.query.all()

    @staticmethod
    def get_product_by_name(name):
        """
        Obtener un producto por su nombre.
        
        Args:
            name (str): Nombre de producto a buscar.
        
        Returns:
            Product: El producto encontrado o None si no existe.
        """
        # Filtrar productos por su nombre (name)
        return Product.query.filter_by(name=name).first()

    @staticmethod
    def get_product_by_id(product_id):
        """
        Obtener un producto por su id.
        
        Args:
            id (int): ID de producto a buscar.
        
        Returns:
            Product: El producto encontrado o None si no existe.
        """
        # Buscar productos por su ID (product_id)
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id, name=None, image=None, description=None, price=None, quantity=None):
        """
        Actualizar los datos de un producto existente.
        
        Args:
            name (str): Nombre del producto a actualizar.
            image (str): Imagen de referencia del producto a actualizar.
            description (str): Descripción del producto a actualizar.
            price (int): Precio del producto a actualizar.
            quantity (int): Cantidad en existencia del producto a actualizar.
        
        Returns:
            None
        
        Raises:
            ValueError: Si el producto no es encontrado.
        """
        # Buscar el producto por su ID
        product = Product.query.get(product_id)
        
        # Si el producto no existe, lanzar un error
        if not product:
            raise ValueError('Product not found')
        
        # Si se proporcionó un nuevo nombre, actualizarlo
        if name:
            product.name = name
        
        # Si se proporcionó una nueva imagen, actualizarla
        if image:
            product.image = image
        
        # Si se proporcionó una nueva descripción, actualizarla
        if description:
            product.description = description
        
        # Si se proporcionó un nuevo precio, actualizarlo
        if price:
            product.price = price

        # Si se proporcionó una nueva cantidad, actualizarla
        if quantity:
            product.quantity = quantity
        
        # Confirmar los cambios y actualizar el producto en la base de datos
        db.session.commit()
        
        return product

    @staticmethod
    def delete_product(product_id):
        """Eliminar un producto existente.
        
        Args:
            product_id (int): El ID del producto a eliminar.

        Raises:
            ValueError: Si el producto no se encuentra.
        """
        # Buscar el producto por su ID
        product = Product.query.get(product_id)
        
        # Si el producto no existe, lanzar un error
        if not product:
            raise ValueError('Product not found')
        
        # Eliminar el producto de la base de datos
        db.session.delete(product)
        
        # Confirmar los cambios
        db.session.commit()

    @staticmethod
    def get_products_by_shop(shop_id):
        """Obtener la lista de productos ofertados por una Tienda específica.
        
        Args:
            shop_id (int): El ID de la Tienda para buscar los productos asociados.

        Returns:
            List[dict]: Lista de diccionarios con los nombres de los productos la Tienda.
        
        Raises:
            ValueError: Si la Tienda no se encuentra.
        """
        # Buscar la Tienda por su ID
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError("Shop not found")
        
        # Obtener los productos asociados a la Tienda
        products = Product.query.filter_by(shop_id=shop.id).all()
        
        # Retornar una lista de nombres de productos
        return products

