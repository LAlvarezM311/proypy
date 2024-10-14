from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.detail_service import SaleDetailService
from flask_jwt_extended import jwt_required

# Namespace para Detalles de Ventas
detail_ns = Namespace('Detalle_Venta', description='Operaciones con los detalles de ventas')

# Modelo de entrada para detalles de ventas
detail_model = detail_ns.model('SaleDetail', {
    'qnt_prod_sale': fields.Integer(required=True, description='Cantidad de productos vendidos asociados al Id de producto'),
    'product_id': fields.List(fields.Integer, description='IDs de los productos asociados'),
    'sale_id': fields.List(fields.Integer, description='IDs de las ventas asociadas')
})

# Modelo de salida para detalle de ventas (respuesta)
detail_response_model = detail_ns.model('SaleDetailResponse', {
    'id': fields.Integer(description='ID del detalle de venta'),
    'qnt_prod_sale': fields.Integer(description='Cantidad de productos vendidos asociados al ID de producto'),
    'product': fields.List(fields.Nested(detail_ns.model('Product', {
        'id': fields.Integer(description='ID del producto'),
        'name': fields.String(description='Nombre del producto')
    })), description='Lista de productos asociados al detalle de venta'),
    'sale': fields.List(fields.Nested(detail_ns.model('Sale', {
        'id': fields.Integer(description='ID de la venta'),
        'date': fields.Date(description='Fecha de la venta')
    })), description='Venta asociada al detalle de venta')
})

@detail_ns.route('/')
class SaleDetailListResource(Resource):
    @jwt_required()
    @detail_ns.marshal_list_with(detail_response_model)  # Serialización automática de la lista de detalle de ventas
    def get(self):
        """Obtener todas los detalles de ventas"""
        details = SaleDetailService.get_all_saledetails()
        return details, 200

    @detail_ns.expect(detail_model, validate=True)
    @jwt_required()
    @detail_ns.marshal_with(detail_response_model, code=201)  # Serialización automática del detalle de venta creado
    def post(self):
        """Crear un nuevo detalle de venta"""
        data = request.get_json()
        detail = SaleDetailService.create_detail(data['qnt_prod_sale'], data['sale_id'], data['product_id'])
        return detail, 201 
