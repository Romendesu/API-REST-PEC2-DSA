from abc import ABC, abstractmethod

class Observer(ABC):
    # Metodo abstracto
    @abstractmethod
    def update(): pass

class ClienteObserver(Observer):
    def update(self, pedido):
        print(f"Cliente notificado: Pedido {pedido.id} ahora está en {pedido.estado}")


class AlmacenObserver(Observer):
    def update(self, pedido):
        print(f"Almacén informado: Preparar pedido {pedido.id}")


class FacturacionObserver(Observer):
    def update(self, pedido):
        print(f"Facturación informada: Actualizar estado del pedido {pedido.id}")