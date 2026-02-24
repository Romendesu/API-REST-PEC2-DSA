
from orders.state import PendingState

class Order:
    # Constructor
    def __init__(self):
        self.id: str = ""
        self.cliente: str = ""
        self.tipo_cliente: str = ""
        self.estado:str = "PENDIENTE"  
        self.items: list = list()
        self.subtotal: float = 0.0
        self.total: float = 0.0
        self.descuento: float = 0.0
        self.metodo_pago: str = ""
        self.creado_en: str = ""
        self._observers = []
        self._state = PendingState(self)

    # Representacion como string
    def __str__(self):
        return f"<Pedido {self.id} - {self.cliente} ({self.tipo_cliente}) - {self.estado} - Total: {self.total}>"
    
    # Añadir observadores
    def add_observer(self, observer):
        self._observers.append(observer)

    # Notificar 
    def notify(self):
        for observer in self._observers:
            observer.update(self)

    # Cambiar el estado del pedido
    def advance(self):
        self._state.advance()

    def cancel(self):
        self._state.cancel()

    # Parsing a diccionario
    def to_dict(self) -> dict:
        descuento = self.subtotal - self.total
        return ({
            "id": self.id,
            "cliente":self.cliente,
            "tipo_cliente":self.tipo_cliente,
            "estado":self.estado,
            "items":self.items,
            "subtotal":self.subtotal,
            "descuento": descuento,
            "total":self.total,
            "metodo_pago":self.metodo_pago,
            "creado_en":self.creado_en
        })
    
    @classmethod
    def from_dict(cls, data: dict):
        from orders.state import PendingState, ProcessingState, ShippedState, DeliveredState, CancelledState
        order = cls()
        order.id = data.get("id", "")
        order.cliente = data.get("cliente", "")
        order.tipo_cliente = data.get("tipo_cliente", "")
        order.estado = data.get("estado", "PENDIENTE")
        order.items = data.get("items", [])
        order.subtotal = data.get("subtotal", 0.0)
        order.descuento = data.get("descuento", 0.0)
        order.total = data.get("total", 0.0)
        order.metodo_pago = data.get("metodo_pago", "")
        order.creado_en = data.get("creado_en", "")
        # Inicializar estado
        if order.estado == "PENDIENTE":
            order._state = PendingState(order)
        elif order.estado == "PROCESANDO":
            order._state = ProcessingState(order)
        elif order.estado == "ENVIADO":
            order._state = ShippedState(order)
        elif order.estado == "ENTREGADO":
            order._state = DeliveredState(order)
        elif order.estado == "CANCELADO":
            order._state = CancelledState(order)
        return order
    