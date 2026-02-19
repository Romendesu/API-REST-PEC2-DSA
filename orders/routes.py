# Rutas para los pedidos
from flask import Blueprint, abort,request

orders = Blueprint('pedidos', __name__)

# Rutas GET
@orders.route("/", methods=["GET"])
def list_all_orders():
    return("Listando todos los pedidos...")

@orders.route("/<id>", methods=["GET"])
def obtain_order_data(id):
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
            abort("500")

# Rutas PUT
@orders.route("/<id>/avanzar", methods=["PUT"])
def set_next_product_state(id):
    return("Pasando al siguiente estado del producto: " + id)

@orders.route("/<id>/cancelar", methods=["PUT"])
def cancel_product(id):
    return("Cancelando el pedido...")
