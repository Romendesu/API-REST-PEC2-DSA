from flask import Blueprint, jsonify, request
import threading
from threading import Lock
from database.database import Database
from utils.constants import HTTP_ACCEPTED, HTTP_CONFLICT, HTTP_NO_CONTENT
from database.structs import Product

products = Blueprint("productos",__name__)
# Variables globales
num_products = 0
products_mutex = threading.Lock()
readDb, writeDb = Database(), Database()
# Rutas GET
@products.route("/", methods=["GET"])
def get_products():
    global readDb
    products = readDb.get_products()
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
    global num_products, products_mutex, writeDb
    data = request.get_json()
    
    # Validacion simple
    if not (data["nombre"] or not data["precio"] or not data["categoria"]):
        return ({
            {
                "STATUS": "CONFLICT",
                "DATA": f"ERROR: INVALID ARGUMENTS",
                "HTTP_STATUS": HTTP_CONFLICT
            }
        })

    # Hacemos que la operación sea atómica
    with products_mutex:
        num_products += 1
        id_product = f"P-{num_products}"
    try:
        data = request.get_json()
        product: dict[Product] = {"id": id, "nombre": data["nombre"], "precio": data["precio"], "categoria": data["categoria"]}

        # Realizamos validacion final
        status = writeDb.add_products(product)

        if (not status):
            return jsonify({
                "STATUS": "CONFLICT",
                "DATA": f"ERROR: SERVER ERROR DURING PARSING ARGUMENTS",
                "HTTP_STATUS": HTTP_CONFLICT
            })
    except Exception as e:
        return jsonify({
                "STATUS": "CONFLICT",
                "DATA": f"ERROR: {e}",
                "HTTP_STATUS": HTTP_CONFLICT
            })
    finally:
        return jsonify({
                "STATUS": "OK",
                "DATA": f"ADDED {product} TO DB",
                "HTTP_STATUS": HTTP_ACCEPTED
            })

