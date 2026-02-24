from abc import ABC, abstractmethod

class OrderState(ABC):
    def __init__(self, order):
        self.order = order

    @abstractmethod
    def advance(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

class PendingState(OrderState):
    def advance(self):
        self.order._state = ProcessingState(self.order)
        self.order.estado = "PROCESANDO"
        self.order.notify()

    def cancel(self):
        self.order._state = CancelledState(self.order)
        self.order.estado = "CANCELADO"
        self.order.notify()

class ProcessingState(OrderState):
    def advance(self):
        self.order._state = ShippedState(self.order)
        self.order.estado = "ENVIADO"
        self.order.notify()

    def cancel(self):
        raise ValueError("No se puede cancelar un pedido en proceso")

class ShippedState(OrderState):
    def advance(self):
        self.order._state = DeliveredState(self.order)
        self.order.estado = "ENTREGADO"
        self.order.notify()

    def cancel(self):
        raise ValueError("No se puede cancelar un pedido enviado")

class DeliveredState(OrderState):
    def advance(self):
        raise ValueError("El pedido ya está entregado")

    def cancel(self):
        raise ValueError("No se puede cancelar un pedido entregado")

class CancelledState(OrderState):
    def advance(self):
        raise ValueError("No se puede avanzar un pedido cancelado")

    def cancel(self):
        raise ValueError("El pedido ya está cancelado")