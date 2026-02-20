from typing import TypedDict

# Estructuras del JSON del Producto
class Product(TypedDict):
    id: str
    nombre: str
    precio: float
    categoria: str

# Estructuras del JSON de Pedidos (REQ)
class OrderReq(TypedDict):
    cliente: str
    tipo_cliente: str
    metodo_pago: str
    items: list[dict]

# Estructuras del JSON de Pedidos (RES)
class OrderRes(TypedDict):
    id: str
    cliente: str
    tipo_cliente:str
    estado:str
    items:list
    subtotal:float
    descuento:float
    total:float
    metodo_pago:str
    creado_en:str