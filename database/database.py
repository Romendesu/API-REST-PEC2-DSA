# Archivo para la creacion de la base de datos
# Funciona como único repositorio
# Emplea el patron de diseño creacional singleton

class DatabaseMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if (cls not in cls._instances):
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=DatabaseMetaClass):
    # Almacenamos los pedidos y productos como atributos privados
    def __init__(self):
        self.__order_buffer = []
        self.__products_buffer = []

    # Metodos no-publicos
    @staticmethod
    def _validate_products_keys():
        ...
    # Metodos publicos
    def get_products(self) -> list:
        return self.__products_buffer
    
    def get_orders(self) -> list:
        return self.__order_buffer
    
    def add_products(self, product:dict) -> str:
        if (not product["id"] or not product["nombre"] or not product["precio"] or not product["categoria"]):
            raise Exception("El formato del JSON no es el especificado")

