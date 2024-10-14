from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.sale_service import SaleService
from flask_jwt_extended import jwt_required

# Namespace para Ventas
sale_ns = Namespace('Ventas', description='Operaciones con las ventas')

# Modelo de entrada para ventas
sale_model = sale_ns.model('Sale', {
    'date': fields.Date(required=True, description='Fecha de la Venta'),
    'total': fields.Integer(description='Valor total de la Venta'),
    'products_ids': fields.List(fields.Integer, description='IDs de los productos asociados')
})

# Modelo de salida para ventas (respuesta)
sale_response_model = sale_ns.model('SaleResponse', {
    'id': fields.Integer(description='ID de la venta'),
    'date': fields.Date(description='Fecha de la Venta'),
    'total': fields.Integer(description='Valor total de la Venta'),
    'status': fields.Integer(description='Estado de la Venta (en proceso, registrada, pagada, anulada)'),
    'products': fields.List(fields.Nested(sale_ns.model('Product', {
        'id': fields.Integer(description='ID del producto'),
        'name': fields.String(description='Nombre del producto')
    })), description='Lista de productos asociados a la venta')
})

@sale_ns.route('/')
class SaleListResource(Resource):
    @jwt_required()
    @sale_ns.marshal_list_with(sale_response_model)  # Serialización automática de la lista de ventas
    def get(self):
        """Obtener todas las ventas"""
        sales = SaleService.get_all_sales()
        return sales, 200

    @sale_ns.expect(sale_model, validate=True)
    @jwt_required()
    @sale_ns.marshal_with(sale_response_model, code=201)  # Serialización automática de la venta creada
    def post(self):
        """Crear una nueva venta"""
        data = request.get_json()
        sale = SaleService.create_sale(data['date'], data['total'], data['products_ids'])
        return sale, 201 
