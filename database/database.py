# Archivo para la creacion de la base de datos
# Funciona como único repositorio
# Emplea el patron de diseño creacional singleton

# Importaciones
from database.structs import OrderReq, OrderRes, Product

# Clase Base de datos
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
    def validate_keys(dict: Dict, req_keys:set):
        for key, key_type in req_keys.items():
            if (key not in dict or not isinstance(dic[key], items)):
                return False
        return True
    # Metodos publicos
    def get_products(self) -> list:
        return self.__products_buffer
    
    def get_orders(self) -> list:
        return self.__order_buffer
    
    def add_products(self, product:dict[Product]) -> bool:
        keys = {"id":str, "nombre":str, "precio":float, "categoria":str}
        json = ()
        # En caso que el formato no sea correcto, se manda error
        if (not validate_keys(product, keys)):
            return False
        
        self.__products_buffer.append(product)
        return True
        

