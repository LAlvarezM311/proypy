from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.shop_service import ShopService

# Crear un espacio de nombres (namespace) para Shop (Tiendas)
shop_ns = Namespace('Shops', description='Operaciones relacionadas con las tiendas')

# Definir el modelo de entrada de shop para la documentación de Swagger
shop_model = shop_ns.model('Shop', {
    'name': fields.String(required=True, description='Nombre de la Tienda'),
    'logo': fields.String(required=True, description='Logo de la Tienda'),
    'description': fields.String(required=True, description='Descripción de la Tienda'),
    'phone': fields.String(required=True, description='Teléfono de la Tienda'),
    'address': fields.String(required=True, description='Dirección de la Tienda'),
    'email': fields.String(required=True, description='Correo Electrónico de la Tienda')
})

# Definir el modelo de salida de shop para la documentación de Swagger
shop_response_model = shop_ns.model('ShopResponse', {
    'id': fields.Integer(description='ID de la Tienda'),
    'name': fields.String(description='Nombre de la Tienda'),
    'logo': fields.String(description='Logo de la Tienda'),
    'description': fields.String(description='Descripción de la Tienda'),
    'phone': fields.String(description='Teléfono de la Tienda'),
    'address': fields.String(description='Dirección de la Tienda'),
    'email': fields.String(description='Correo Electrónico de la Tienda')
})

# Definir el modelo de salida para product
product_response_model = shop_ns.model('ProductResponse', {
    'name': fields.String(description='Nombre del Producto')
})

# Controlador para manejar las operaciones CRUD de shop
@shop_ns.route('/')
class ShopListResource(Resource):
    @shop_ns.doc('get_shops')
    @shop_ns.marshal_list_with(shop_response_model)  # Decorador para definir el formato de la respuesta
    def get(self):
        """Obtener todas las Tiendas"""
        shops = ShopService.get_all_shops()
        return shops, 200

    @shop_ns.doc('create_shop')
    @shop_ns.expect(shop_model, validate=True)  # Decorador para esperar el modelo en la solicitud
    @shop_ns.marshal_with(shop_response_model, code=201)  # Decorador para definir el formato de la respuesta
    def post(self):
        """Crear una nueva Tienda"""
        data = request.get_json()
        try:
            shop = ShopService.create_shop(data['name'], data['logo'], data['description'], data['phone'], data['address'], data['email'])
            return shop, 201
        except ValueError as e:
            return {'message': str(e)}, 400

@shop_ns.route('/<int:shop_id>')
@shop_ns.param('shop_id', 'El ID de la Tienda')
class ShopResource(Resource):
    @shop_ns.doc('get_shop_by_id')
    @shop_ns.marshal_with(shop_response_model)
    def get(self, shop_id):
        """Obtener una Tienda por su ID"""
        shop = ShopService.get_shop_by_id(shop_id)
        if not shop:
            return {'message': 'Shop not found'}, 404
        return shop, 200

    @shop_ns.doc('update_shop')
    @shop_ns.expect(shop_model, validate=True)  # Esperar los nuevos datos de la tienda
    @shop_ns.marshal_with(shop_response_model)
    def put(self, shop_id):
        """Actualizar una tienda por su ID"""
        data = request.get_json()
        try:
            shop = ShopService.update_shop(shop_id, data['name'])
            return shop, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @shop_ns.doc('delete_shop')
    def delete(self, shop_id):
        """Eliminar una Tienda por su ID"""
        try:
            ShopService.delete_shop(shop_id)
            return {'message': 'Shop deleted successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404


