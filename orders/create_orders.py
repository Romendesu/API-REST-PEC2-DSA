# Empleo del patrón de diseño "builder" para construir pedidos
# Estructura del pedido:
'''
{
  "id": "ord-001",
  "cliente": "Ana García",
  "tipo_cliente": "premium",
  "estado": "PENDIENTE",
  "items": [...],
  "subtotal": 2400.00,
  "descuento": 240.00,
  "total": 2160.00,
  "metodo_pago": "PayPal",
  "creado_en": "2025-01-15T10:30:00"
}

'''
from datetime import datetime

class Order:
    def __init__(self):
        self.id: str = ""
        self.cliente: str = ""
        self.tipo_cliente: str = ""
        self.estado:str = "PENDIENTE"  
        self.items: list = list()
        self.subtotal: float = 0.0
        self.total: float = 0.0
        self.metodo_pago: str = ""
        self.creado_en: str = ""

    def __str__(self):
        return f"<Pedido {self.id} - {self.cliente} ({self.tipo_cliente}) - {self.estado} - Total: {self.total}>"
    
    # Parsing a diccionario
    def to_dict(self) -> dict:
        return ({
            "id": self.id,
            "cliente":self.cliente,
            "tipo_cliente":self.tipo_cliente,
            "estado":self.estado,
            "items":self.items,
            "subtotal":self.subtotal,
            "total":self.total,
            "metodo_pago":self.metodo_pago,
            "creado_en":self.creado_en

        })
    
class OrderBuilder:
    # Constructor
    def __init__(self):
        self.order = Order()

    # Metodo para construir el ID del cliente
    def set_id(self, id_pedido: str):
        self.order.id = id_pedido
        return self

    # Metodo para establecer el nombre del cliente y su tipo
    def set_cliente(self, cliente: str, tipo_cliente: str="normal"):
        self.order.cliente = cliente
        self.order.tipo_cliente = tipo_cliente
        return self

    # Metodo para agregar un producto
    def agregar_producto(self, producto, precio, cantidad=1):
        self.order.items.append({"producto": producto, "precio": precio, "cantidad": cantidad})
        self.order.subtotal += precio * cantidad
        return self

    # Metodo para aplicar un descuento determinado
    def aplicar_descuento(self, porcentaje):
        self.order.total = self.order.subtotal * (1 - porcentaje / 100)
        return self

    # Metodo para establecer un metodo de pago 
    def set_metodo_pago(self, metodo_pago):
        self.order.metodo_pago = metodo_pago
        return self

    # Metodo para establecer una fecha
    def set_creado_en(self):
        self.order.creado_en =  datetime.utcnow().isoformat()
        return self
    
    # Builder
    def build(self):
        # Validaciones -> Productos y Cliente
        if not (self.order.items):
            raise ValueError("El pedido debe tener como mínimo 1 producto")
        if not (self.order.cliente):
            raise ValueError("El pedido debe tener como mínimo 1 cliente")
        
        # Si no existe un descuento, se aplica que el subtotal = total
        if (self.order.total == 0):
            self.order.total = self.order.subtotal
        
        # Regresamos el pedido construido
        return self.order

