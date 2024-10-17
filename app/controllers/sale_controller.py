from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.sale_service import SaleService
from app.models.sale import StateEnum
from flask_jwt_extended import jwt_required

# Namespace para Ventas
sale_ns = Namespace('Ventas', description='Operaciones con las ventas')

# Modelo de entrada para ventas
sale_model = sale_ns.model('Sales', {
    'date': fields.Date(required=True, description='Fecha de la Venta'),
    'total': fields.Integer(description='Valor total de la Venta'),
    'status': fields.Integer(description='Estado de la Venta (0: en proceso, 1: registrada, 2: pagada, 3: anulada)'),
   
})

# Modelo de salida para ventas (respuesta)
sale_response_model = sale_ns.model('SalesResponse', {
    'id': fields.Integer(description='ID de la venta'),
    'date': fields.Date(description='Fecha de la Venta'),
    'total': fields.Integer(description='Valor total de la Venta'),
    'status': fields.String(description='Estado de la Venta (en proceso, registrada, pagada, anulada)'),
    
})


def map_status_to_enum(status_int):
    """Mapea un valor entero a su correspondiente valor del enum StateEnum."""
    try:
        return StateEnum(status_int)
    except ValueError:
        raise ValueError(f"Estado no válido: {status_int}. Valores permitidos: 0, 1, 2, 3.")

def map_enum_to_status(enum_value):
    """Mapea el enum a su representación como cadena."""
    status_map = {
        StateEnum.IN_PROGRESS: "En proceso",
        StateEnum.REGISTERED: "Registrada",
        StateEnum.PAID: "Pagada",
        StateEnum.NULLED: "Anulada"
    }
    return status_map.get(enum_value, "Desconocido")

@sale_ns.route('/')
class SaleListResource(Resource):
    #@jwt_required()
    @sale_ns.marshal_list_with(sale_response_model)  # Serialización automática de la lista de ventas
    def get(self):
        """Obtener todas las ventas"""
        sales = SaleService.get_all_sales()
                # Mapeo de status de enum a cadena para la respuesta
        for sale in sales:
            sale.status = map_enum_to_status(sale.status)
        return sales, 200

    @sale_ns.expect(sale_model, validate=True)
    #@jwt_required()
    @sale_ns.marshal_with(sale_response_model, code=201)  # Serialización automática de la venta creada
    def post(self):
        """Crear una nueva venta"""
        data = request.get_json()

    # Convertir el status a enum
        try:
            status_enum = map_status_to_enum(data['status'])
        except ValueError as e:
            return {'message': str(e)}, 400
    # Crear la venta
        sale = SaleService.create_sale(data['date'], data['total'], status_enum)
    
     # Mapeo de status para la respuesta
        sale.status = map_enum_to_status(sale.status)

        return sale, 201 

@sale_ns.route('/<int:sale_id>')
@sale_ns.param('sale_id', 'El ID de la Venta')
class SaleResource(Resource):
    @sale_ns.expect(sale_model, validate=True)
    @sale_ns.marshal_with(sale_response_model)
    def put(self, sale_id):
        """Actualizar una venta por su ID"""
        data = request.get_json()  # Obtiene los nuevos datos para la venta

 # Convertir el status a enum
        try:
            status_enum = map_status_to_enum(data['status'])
        except ValueError as e:
            return {'message': str(e)}, 400

        sale = SaleService.update_sale(sale_id, data['date'], data['total'], status_enum)  # Llama al servicio para actualizar
        # Mapeo de status para la respuesta
        sale.status = map_enum_to_status(sale.status)
        return sale, 200  # Retorna la venta actualizada con un código de estado 200 (OK)

    
    def delete(self, sale_id):
        """Eliminar una venta por su ID"""
        try:
            SaleService.delete_sale(sale_id)  # Llama al servicio para eliminar la venta
            return {'message': 'Venta eliminada correctamente'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404
