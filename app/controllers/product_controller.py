from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.product_service import ProductService

# Crear un espacio de nombres (namespace) para Product (Productos)
product_ns = Namespace('Products', description='Operaciones relacionadas con los productos')

# Definir el modelo de entrada de product para la documentación de Swagger
product_model = product_ns.model('Product', {
    'name': fields.String(required=True, description='Nombre del Producto'),
    'image': fields.String(required=True, description='Imagen del Producto'),
    'description': fields.String(required=True, description='Descripción del Producto'),
    'price': fields.Integer(required=True, description='Precio del Producto'),
    'quantity': fields.Integer(required=True, description='Cantidad en existencia del Producto'),
    'shop_id': fields.Integer(required=True, description='Id de la tienda a la queu pertenece el producto')
})

# Definir el modelo de salida de product para la documentación de Swagger
product_response_model = product_ns.model('ProductResponse', {
    'id': fields.Integer(description='ID del Producto'),
    'image': fields.String(required=True, description='Imagen del Producto'),
    'description': fields.String(required=True, description='Descripción del Producto'),
    'price': fields.Integer(required=True, description='Precio del Producto'),
    'quantity': fields.Integer(required=True, description='Cantidad en existencia del Producto'),
    'shops': fields.List(fields.Nested(product_ns.model('Shop', {
        'id': fields.Integer(description='ID de la tienda'),
        'name': fields.String(description='Nombre de la tienda')
    })), description='Lista de tienda asociada al producto')
})


# Controlador para manejar las operaciones CRUD de product
@product_ns.route('/')
class ProductListResource(Resource):
    # Método para obtener todos los productos registrados
    @product_ns.doc('get_products')
    @product_ns.marshal_list_with(product_response_model)  # Decorador para definir el formato de la respuesta
    def get(self):
        """Obtener todos los Productos"""
        products = ProductService.get_all_products()
        return products, 200
    # Método para crear un nuevo producto
    @product_ns.doc('create_product')
    @product_ns.expect(product_model, validate=True)  # Decorador para esperar el modelo en la solicitud
    @product_ns.marshal_with(product_response_model, code=201)  # Decorador para definir el formato de la respuesta
    def post(self):
        """Crear un nuevo Producto"""
        data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud

        product = ProductService.create_product(
            data['name'], 
            data['image'], 
            data['description'], 
            data['price'], 
            data['quantity'], 
            data['shop_id'])
        return product, 201
        # Usamos jsonify para asegurarnos de que la respuesta siga el formato JSON válido.

@product_ns.route('/<int:product_id>')
@product_ns.param('product_id', 'El ID del Producto')
class ProductResource(Resource):
    @product_ns.doc('get_product_by_id')
    @product_ns.marshal_with(product_response_model)
    def get(self, product_id):
        """Obtener un Producto por su ID"""
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        return product, 200

    @product_ns.doc('update_product')
    @product_ns.expect(product_model, validate=True)  # Esperar los nuevos datos del producto
    @product_ns.marshal_with(product_response_model)
    def put(self, product_id):
        """Actualizar un producto por su ID"""
        data = request.get_json()
        try:
            product = ProductService.update_product(product_id, data['name'])
            return product, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @product_ns.doc('delete_product')
    def delete(self, product_id):
        """Eliminar un Producto por su ID"""
        try:
            ProductService.delete_product(product_id)
            return {'message': 'Product deleted successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404


@product_ns.route('/<int:shop_id>/products')
@product_ns.param('shop_id', 'El ID de la Tienda')
class ShopProductResource(Resource):
    @product_ns.doc('get_product_by_shop')
    @product_ns.marshal_list_with(product_response_model)
    def get(self, shop_id):
        """Obtener todos los productos que están asignados a una tienda específica"""
        try:
            products = ProductService.get_products_by_shop(shop_id)
            return products, 200
        except ValueError as e:
            return {'message': str(e)}, 404

