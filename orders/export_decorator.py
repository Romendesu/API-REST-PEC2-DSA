from abc import ABC, abstractmethod
import json

class OrderExporter(ABC):
    @abstractmethod
    def export(self, order: dict) -> str:
        pass

class JSONExporter(OrderExporter):
    def export(self, order: dict) -> str:
        return json.dumps(order, indent=4)

class TextExporter(OrderExporter):
    def export(self, order: dict) -> str:
        text = f"Pedido ID: {order['id']}\n"
        text += f"Cliente: {order['cliente']} ({order['tipo_cliente']})\n"
        text += f"Estado: {order['estado']}\n"
        text += f"Items:\n"
        for item in order['items']:
            text += f"  - {item['producto']}: {item['cantidad']} x {item['precio']} = {item['cantidad'] * item['precio']}\n"
        text += f"Subtotal: {order['subtotal']}\n"
        text += f"Total: {order['total']}\n"
        text += f"Método de Pago: {order['metodo_pago']}\n"
        text += f"Creado en: {order['creado_en']}\n"
        return text

class ExporterFactory:
    @staticmethod
    def get_exporter(format_type: str) -> OrderExporter:
        if format_type == "json":
            return JSONExporter()
        elif format_type == "text":
            return TextExporter()
        else:
            raise ValueError(f"Formato no soportado: {format_type}")