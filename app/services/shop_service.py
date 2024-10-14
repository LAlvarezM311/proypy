from app import db
from app.models.shop import Shop


class ShopService:
    """Servicio para manejar las operaciones CRUD y adicionales para shops."""

    @staticmethod
    def create_shop(name, logo, description, phone, address, email):
        """Crear una nueva Tienda (Shop) en la base de datos.
        
        Args:
            name (str): El nombre de la nueva tienda.
            logo (str): El logo de la Tienda.
            description (str): Descripción de la tienda.
            phone (str): número de teléfono de la tienda.
            address (str): Dirección de la tienda.
            email (str): Correo electrónico de la tienda.

        Returns:
            Shop: La nueva tienda creada.

        Raises:
            ValueError: Si la tienda ya existe.
        """
        # Verificar si la tienda ya existe
        shop = Shop.query.filter_by(name=name).first()
        if shop:
            raise ValueError("Shop already exists")
        
        # Crear una nueva Tienda
        new_shop = Shop(name=name, logo=logo, description=description, phone=phone, address=address, email=email)
        
        # Guardar la Tienda en la base de datos
        db.session.add(new_shop)
        db.session.commit()
        
        return new_shop

    @staticmethod
    def get_all_shops():
        """Obtener todas las Tiendas disponibles.
        
        Returns:
            List[Shop]: Lista de todas las Tiendas en la base de datos.
        """
        # Retorna todas las Tiendas
        return Shop.query.all()

    @staticmethod
    def get_shop_by_id(shop_id):
        """Obtener una tienda por su ID.
        
        Args:
            shop_id (int): El ID de la Tienda.

        Returns:
            Shop: La Tienda correspondiente al ID, o None si no existe.
        """
        # Buscar la Tienda por su ID
        return Shop.query.get(shop_id)

    @staticmethod
    def update_shop(shop_id, new_name):
        """Actualizar el nombre de una tienda existente.
        
        Args:
            shop_id (int): El ID de la Tienda a actualizar.
            new_name (str): El nuevo nombre para la Tienda.

        Returns:
            Shop: La Tienda actualizada.

        Raises:
            ValueError: Si la Tienda no se encuentra.
        """
        # Buscar la Tienda por su ID
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError("Shop not found")
        
        # Actualizar el nombre de la Tienda
        shop.name = new_name
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return shop

    @staticmethod
    def delete_shop(shop_id):
        """Eliminar una Tienda existente de la base de datos.
        
        Args:
            shop_id (int): El ID de la Tienda a eliminar.

        Raises:
            ValueError: Si la Tienda no se encuentra.
        """
        # Buscar la Tienda por su ID
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError("Shop not found")
        
        # Eliminar la Tienda
        db.session.delete(shop)
        db.session.commit()


