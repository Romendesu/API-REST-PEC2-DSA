from flask import Blueprint, jsonify
from database.database import Database
from utils.constants import HTTP_ACCEPTED, HTTP_CONFLICT, HTTP_NO_CONTENT
products = Blueprint("productos",__name__)

# Rutas GET
@products.route("/", methods=["GET"])
def get_products():
    db = Database()
    products = db.get_products()
    json = dict()
    try:
        if (products):
            json = {
                "STATUS": "OK",
                "DATA": products,
                "HTTP_STATUS": HTTP_ACCEPTED
            }
        else:
            json = {
                "STATUS": "NO CONTENT",
                "DATA": "No se han encontrado productos",
                "HTTP_STATUS": HTTP_NO_CONTENT
            }
    except Exception as e:
        json = {
                "STATUS": "CONFLICT",
                "DATA": f"ERROR: {e}",
                "HTTP_STATUS": HTTP_CONFLICT
            }
    finally:
        return(jsonify(json))
            

# Rutas POST
@products.route("/", methods=["POST"])
def create_product():
    return("Creando producto")

