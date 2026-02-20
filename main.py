# Archivo para ejecutar el python
from flask import Flask
from flask_cors import CORS
from orders.routes import orders
from products.routes import products

def create_app() -> Flask:
    app = Flask(__name__)
    # Registramos cada blueprint
    app.register_blueprint(orders, url_prefix="/pedidos")
    app.register_blueprint(products, url_prefix="/productos")

    CORS(app)
    # Establecemos la ruta raiz como una bienvenida al usuario (Punto de entrada)
    @app.route("/")
    def main_route():
        return("<h1> Bienvenido a la ruta raiz</h1><p>Empieza a usar la API leyendo la documentación.</p>")

    return app

def main() -> None:
    app = create_app()
    app.run(debug=True)

if __name__=="__main__":
    main()