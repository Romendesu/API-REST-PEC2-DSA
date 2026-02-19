# Rutas para los pedidos
from flask import Blueprint, abort, request, jsonify
from database.database import Database
from utils.constants import HTTP_ACCEPTED, HTTP_CONFLICT, HTTP_NO_CONTENT
# Definicion de modulos a emplear
orders = Blueprint('pedidos', __name__)

# Rutas GET
@orders.route("/", methods=["GET"])
def get_orders():
    # LLamamos a la base de datos
    db = Database()
    orders = db.get_orders()
    json = dict()
    # Manejamos la orden 
    try:
        if (orders):
            json = {
                "STATUS": "OK",
                "DATA": orders,
                "HTTP_STATUS": HTTP_ACCEPTED
            }
        else:
            json = {
                "STATUS": "NO CONTENT",
                "DATA": "No hay pedidos disponibles",
                "HTTP_STATUS": HTTP_NO_CONTENT
            }
    except Exception as e:
        json = {
            "STATUS": "ERROR",
            "INFO": f"ERROR: {e}",
            "HTTP_STcancel_productATUS": HTTP_CONFLICT
        }
    finally:
        return(jsonify(json))

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
            abort("500")

# Rutas PUT
@orders.route("/<id>/avanzar", methods=["PUT"])
def update_product_state(id):
    return("Pasando al siguiente estado del producto: " + id)

@orders.route("/<id>/cancelar", methods=["PUT"])
def delete_product(id):
    return("Cancelando el pedido...")
