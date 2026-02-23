from flask import Blueprint, request
from utils.response import ResponseFactory
from database.database import db

products = Blueprint("productos",__name__)

# Rutas GET
@products.route("/", methods=["GET"])
def get_products():
    products = db.get_products()
    try:
        if (products):
            return ResponseFactory.ok(data=products)
        else:
            return ResponseFactory.no_content(message="No se han encontrado productos")
    except Exception as e:
        return ResponseFactory.error(message=f"ERROR: {e}")
            

# Rutas POST
@products.route("/", methods=["POST"])
def create_product():
    product = request.get_json()
    # Si no hay producto, lanzamos error
    if not (product):
        return ResponseFactory.error(message="No se recibió el archivo JSON")
    
    # Si se ha creado el producto, mandamos un mensaje de exito
    isProductAdded = db.add_products(product=product)
    if (isProductAdded):
        return ResponseFactory.ok(data=product, message=f"EXITO: SE HA AÑADIDO: {product}")
    
    # Error en caso de conflicto
    return ResponseFactory.conflict(f"ERROR: No se ha podido agregar {product}")
    


