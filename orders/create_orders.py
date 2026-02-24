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
from orders.order import Order
from orders.discount_strategy import DiscountFactory
from utils.payment_factory import PaymentFactory

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
        
        # Aplicar descuento según tipo de cliente
        strategy = DiscountFactory.get_strategy(self.order.tipo_cliente)
        self.order.total = strategy.apply_discount(self.order.subtotal)
        self.order.descuento = self.order.subtotal - self.order.total
        
        # Procesar pago
        payment = PaymentFactory.create_payment(self.order.metodo_pago)
        if not payment.process(self.order.total):
            raise ValueError("Error al procesar el pago")
        
        # Regresamos el pedido construido
        return self.order

