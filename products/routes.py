from flask import Blueprint

products = Blueprint("productos",__name__)

# Rutas GET
@products.route("/", methods=["GET"])
def list_all_products():
    return("Listando todos los productos")

# Rutas POST
@products.route("/", methods=["POST"])
def create_product():
    return("Creando producto")

