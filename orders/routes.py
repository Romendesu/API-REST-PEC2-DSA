# Rutas para los pedidos
from flask import Blueprint, abort, request
from utils.response import ResponseFactory
from orders.create_orders import OrderBuilder
from orders.order import Order
from orders.observer import AlmacenObserver, ClienteObserver, FacturacionObserver
from orders.export_decorator import ExporterFactory
from database.database import db

# Definicion de modulos a emplear
orders = Blueprint('pedidos', __name__)

# Rutas GET
@orders.route("/", methods=["GET"])
def get_orders():
    # LLamamos a la base de datos
    orders = db.get_orders()
    try:
        # Si existe el pedido, lo listamos, sino no se devuelve nada
        if (orders):
            return ResponseFactory.ok(orders)
        else:
            return ResponseFactory.no_content()
        
    # Si falla el get, mandamos error
    except Exception as e:
        return ResponseFactory.error(message=f"ERROR: Se ha producido un error interno,\n{e}")
    
@orders.route("/<id>", methods=["GET"])
def get_order(id):
    try:
        order = db.get_specific_order(id)
        if (order):
            return ResponseFactory.ok(order)
        return ResponseFactory.error("No existe el pedido")
    except Exception as e:
        return ResponseFactory.conflict(f"Se ha producido una excepcion: {e}")

@orders.route("/<id>/exportar", methods=["GET"])
def export_data(id):
    format_type = request.args.get("formato")
    try:
        order_dict = db.get_specific_order(id)
        if not order_dict:
            return ResponseFactory.error("No existe el pedido")
        
        exporter = ExporterFactory.get_exporter(format_type)
        exported_data = exporter.export(order_dict)
        return ResponseFactory.ok(exported_data)
    except Exception as e:
        return ResponseFactory.error(f"Error al exportar: {e}")

# Rutas PUT
@orders.route("/<id>/avanzar", methods=["PUT"])
def update_product_state(id):
    try:
        order_dict = db.get_specific_order(id)
        if not order_dict:
            return ResponseFactory.error("No existe el pedido")
        
        # Convertir a objeto Order
        order = Order.from_dict(order_dict)
        
        # Añadir observadores
        order.add_observer(ClienteObserver())
        order.add_observer(AlmacenObserver())
        order.add_observer(FacturacionObserver())
        
        # Avanzar estado
        order.advance()
        
        # Actualizar en DB
        updated_dict = order.to_dict()
        db.update_order(id, updated_dict)
        
        return ResponseFactory.ok(updated_dict)
        
    except Exception as e:
        return ResponseFactory.conflict(f"Se ha producido una excepcion: {e}")
    

@orders.route("/<id>/cancelar", methods=["PUT"])
def delete_product(id):
    try:
        order_dict = db.get_specific_order(id)
        if not order_dict:
            return ResponseFactory.error("No existe el pedido")
        
        # Convertir a objeto Order
        order = Order.from_dict(order_dict)
        
        # Añadir observadores
        order.add_observer(ClienteObserver())
        order.add_observer(AlmacenObserver())
        order.add_observer(FacturacionObserver())
        
        # Cancelar pedido
        order.cancel()
        
        # Actualizar en DB
        updated_dict = order.to_dict()
        db.update_order(id, updated_dict)
        
        return ResponseFactory.ok(updated_dict)
        
    except Exception as e:
        return ResponseFactory.conflict(f"Se ha producido una excepcion: {e}")

# RUTAS POST
@orders.route("/", methods=["POST"])
def add_orders():
    data = request.get_json()
    try:
        builder = OrderBuilder()
        # Agregar el tipo de cliente y el metodo de pago
        builder.set_cliente(data["cliente"], data.get("tipo_cliente"))
        builder.set_metodo_pago(data.get("metodo_pago"))            

        # Agregar productos
        for item in data.get("items", []):
            producto_id = item["producto_id"]
            cantidad = item.get("cantidad", 1)
            # Obtener el pedido 
            product = db.get_specific_product(producto_id)
            if (product):
                precio = product["precio"]
                builder.agregar_producto(producto_id, precio, cantidad)

        # Agregar el TS
        builder.set_creado_en()

        # Construimos el pedido
        final_order = builder.build()

        # Registrar observers
        final_order.add_observer(ClienteObserver())
        final_order.add_observer(AlmacenObserver())
        final_order.add_observer(FacturacionObserver())

        order_dict = final_order.to_dict()
        db.add_orders(order_dict)
        return ResponseFactory.ok(order_dict)
    
    # En caso de error:
    except Exception as e:
        return ResponseFactory.error(f"ERROR: se ha producido un error\n{e}")