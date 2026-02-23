# Archivo para la creacion de la base de datos
# Funciona como único repositorio
# Emplea el patron de diseño creacional Singleton

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
        self.__order_buffer = list()
        self.__products_buffer = list()

    '''
    ============================================================================
    MÉTODOS AUXILIARES: COMPROBACIONES Y OPERACIONES QUE SE REPITAN
    ============================================================================
    '''

    @staticmethod
    def _validate_keys(data:dict, keys:list):
        # Se validan las claves
        for key in keys:
            if not (key in data and data[key] not in (None, "")):
                return False
        return True

                
            
        
    '''
    ============================================================================
    MÉTODOS PUBLICOS: 
    1) Operaciones de acceso y escritura en la base de datos    -> [get, set]
    2) Operaciones de agregación y descarte en la base de datos -> [add, remove]
    ============================================================================
    '''
    # Obtener longitud
    def length_orders(self) -> int:
        return len(self.__order_buffer)
    
    # Obtener todos los productos
    def get_products(self) -> list:
        return self.__products_buffer
    
    # Obtener solo un producto en especifico
    def get_specific_product(self, product_id: str) -> dict|None:
        for element in self.__products_buffer:
            if (element["id"] == product_id):
                return element
            
    # Obtener todas las ordenes
    def get_orders(self) -> list:
        return self.__order_buffer
    
    # Obtener solo un producto en especifico
    def get_specific_order(self, order_id: str) -> dict|None:
        for element in self.__order_buffer:
            if (element["id"] == order_id):
                return element

    # Añadir productos      
    def add_products(self, product:dict) -> bool:
        products_keys = ["nombre","precio","categoria" ]
        # Si el formato no es correcto, devolvemos error
        if not(self._validate_keys(product, products_keys)):
            print("ERROR: EL FORMATO NO ES CORRECTO")
            return False
        
        # Asignamos el ID
        product["id"] = f"p{len(self.__products_buffer)}"
        self.__products_buffer.append(product)
        print("EXITO: SE HA AÑADIDO EL PRODUCTO")
        return True

    # Añadir pedidos    
    def add_orders(self,order:dict) -> bool:
        order_keys = ["id", "cliente", "tipo_cliente", "estado","items","subtotal","descuento","total", "metodo_pago", "creado_en"]
        if not(self._validate_keys(order, order_keys)):
            print("ERROR: EL FORMATO NO ES CORRECTO ")
            return False
        
        order["id"] = f"p{len(self.__order_buffer)}"
        self.__order_buffer.append(order)
        print("EXITO: SE HA AÑADIDO EL PEDIDO")
        return True

db = Database()