from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.detail_service import SaleDetailService
from flask_jwt_extended import jwt_required

# Namespace para Detalles de Ventas
detail_ns = Namespace('Detalles_Venta', description='Operaciones con los detalles de ventas')

# Modelo de entrada para detalles de ventas
detail_model = detail_ns.model('SalesDetail', {
    'qnt_prod_sale': fields.Integer(required=True, description='Cantidad de productos vendidos asociados al Id de producto'),
    'sale_id': fields.Integer(required=True, description='IDs de las ventas asociadas'),
    'product_id': fields.Integer(required=True, description='IDs de los productos asociados')
    
})

# Modelo de salida para detalle de ventas (respuesta)
detail_response_model = detail_ns.model('SalesDetailResponse', {
    'id': fields.Integer(description='ID del detalle de venta'),
    'qnt_prod_sale': fields.Integer(description='Cantidad de productos vendidos asociados al ID de producto'),
    'sale_id': fields.Integer(required=True, description='IDs de las ventas asociadas'),
    'product_id': fields.Integer(required=True, description='IDs de los productos asociados')
    
})

@detail_ns.route('/')
class SaleDetailListResource(Resource):
    
    @detail_ns.marshal_list_with(detail_response_model)  # Serialización automática de la lista de detalle de ventas
    def get(self):
        """Obtener todas los detalles de ventas"""
        details = SaleDetailService.get_all_saledetails()
        return details, 200

    @detail_ns.expect(detail_model, validate=True)
    
    @detail_ns.marshal_with(detail_response_model, code=201)  # Serialización automática del detalle de venta creado
    def post(self):
        """Crear un nuevo detalle de venta"""
        data = request.get_json()
        detail = SaleDetailService.create_detail(data['qnt_prod_sale'], data['sale_id'], data['product_id'])
        return detail, 201 

@detail_ns.route('/<int:id>')
@detail_ns.param('id', 'El ID del detalle')
class SaleDetailResource(Resource):
    @detail_ns.expect(detail_model, validate=True)
    @detail_ns.marshal_with(detail_response_model)
    def put(self, id):
        """Actualizar un detalle de venta por su ID"""
        data = request.get_json()  # Obtiene los nuevos datos para el detalle de venta

        try:
            detail = SaleDetailService.update_detail(id, data['qnt_prod_sale'], data['sale_id'], data['product_id'])  # Llama al servicio para actualizar

            return detail, 200  # Retorna la venta actualizada con un código de estado 200 (OK)
        except ValueError as e:
            return {'message': str(e)}, 404 


    
    def delete(self, id):
        """Eliminar un detalle de venta por su ID"""
        try:
            SaleDetailService.delete_detail(id)  # Llama al servicio para eliminar el detalle de venta
            return {'message': 'Detalle de Venta eliminado correctamente'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404