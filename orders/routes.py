# Rutas para los pedidos
from flask import Blueprint, abort, request
from utils.response import ResponseFactory
from orders.create_orders import OrderBuilder
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
    return("Datos del pedido: " + id)

@orders.route("/<id>/exportar", methods=["GET"])
def export_data(id):
    format = request.args.get("formato")
    match (format):
        case "json":
            return("Exportando en formato JSON del pedido: ",id)
        case "text":
            return("Exportando en texto plano del pedido: ",id)
        case _:
            abort(500)

# Rutas PUT
@orders.route("/<id>/avanzar", methods=["PUT"])
def update_product_state(id):
    return("Pasando al siguiente estado del producto: " + id)

@orders.route("/<id>/cancelar", methods=["PUT"])
def delete_product(id):
    return("Cancelando el pedido...")

# RUTAS POST
@orders.route("/", methods=["POST"])
def add_orders():
    data = request.get_json()
    try:
        builder = OrderBuilder()
        # Agregar el tipo de cliente y el metodo de pago
        builder.set_id(f"ord-f{db.length_orders()}")
        builder.set_cliente(data["cliente"], data.get("tipo_cliente"))
        builder.set_metodo_pago(data.get("metodo_pago"))            # De momento...

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
        final_order = builder.build().to_dict()

        # Añadir los campos obligatorios si aún no existen
        if "descuento" not in final_order:
            final_order["descuento"] = 0.0
        if "total" not in final_order:
            final_order["total"] = final_order["subtotal"]

        # Añadir el pedido a la base de datos
        db.add_orders(final_order)
        return ResponseFactory.ok(final_order)
    
    # En caso de error:
    except Exception as e:
        return ResponseFactory.error(f"ERROR: se ha producido un error\n{e}")