import unittest
import json
from main import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Crear un producto para usar en pedidos
        product_data = {
            "nombre": "Producto Base",
            "precio": 50.0,
            "categoria": "Base"
        }
        self.client.post('/productos/', json=product_data)

    def test_create_product(self):
        data = {
            "nombre": "Producto Test",
            "precio": 100.0,
            "categoria": "Test"
        }
        response = self.client.post('/productos/', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("EXITO", response.get_json()['MESSAGE'])

    def test_get_products(self):
        response = self.client.get('/productos/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json()['DATA'], list)

    def test_create_order(self):
        # Primero crear un producto
        product_data = {
            "nombre": "Producto Pedido",
            "precio": 50.0,
            "categoria": "Pedido"
        }
        self.client.post('/productos/', json=product_data)

        # Crear pedido
        order_data = {
            "cliente": "Cliente Test",
            "tipo_cliente": "premium",
            "metodo_pago": "PayPal",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 2
                }
            ]
        }
        response = self.client.post('/pedidos/', json=order_data)
        self.assertEqual(response.status_code, 200)
        order = response.get_json()['DATA']
        self.assertEqual(order['estado'], 'PENDIENTE')
        self.assertEqual(order['total'], 90.0)  # 100 * 0.9 descuento premium

    def test_advance_order(self):
        # Crear pedido
        order_data = {
            "cliente": "Cliente Test",
            "tipo_cliente": "normal",
            "metodo_pago": "tarjeta de crédito",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 1
                }
            ]
        }
        create_response = self.client.post('/pedidos/', json=order_data)
        order_id = create_response.get_json()['DATA']['id']

        # Avanzar estado
        response = self.client.put(f'/pedidos/{order_id}/avanzar')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['DATA']['estado'], 'PROCESANDO')

    def test_cancel_order(self):
        # Crear pedido
        order_data = {
            "cliente": "Cliente Test",
            "tipo_cliente": "normal",
            "metodo_pago": "transferencia bancaria",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 1
                }
            ]
        }
        create_response = self.client.post('/pedidos/', json=order_data)
        order_id = create_response.get_json()['DATA']['id']

        # Cancelar
        response = self.client.put(f'/pedidos/{order_id}/cancelar')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['DATA']['estado'], 'CANCELADO')

    def test_export_order_json(self):
        # Crear pedido
        order_data = {
            "cliente": "Cliente Test",
            "tipo_cliente": "normal",
            "metodo_pago": "PayPal",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 1
                }
            ]
        }
        create_response = self.client.post('/pedidos/', json=order_data)
        order_id = create_response.get_json()['DATA']['id']

        # Exportar JSON
        response = self.client.get(f'/pedidos/{order_id}/exportar?formato=json')
        self.assertEqual(response.status_code, 200)
        exported = json.loads(response.get_json()['DATA'])
        self.assertEqual(exported['id'], order_id)

    def test_export_order_text(self):
        # Crear pedido
        order_data = {
            "cliente": "Cliente Test",
            "tipo_cliente": "normal",
            "metodo_pago": "tarjeta de crédito",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 1
                }
            ]
        }
        create_response = self.client.post('/pedidos/', json=order_data)
        order_id = create_response.get_json()['DATA']['id']

        # Exportar texto
        response = self.client.get(f'/pedidos/{order_id}/exportar?formato=text')
        self.assertEqual(response.status_code, 200)
        exported = response.get_json()['DATA']
        self.assertIn("Pedido ID:", exported)

    def test_discounts(self):
        # Test descuento normal (0%)
        order_data = {
            "cliente": "Cliente Normal",
            "tipo_cliente": "normal",
            "metodo_pago": "PayPal",
            "items": [
                {
                    "producto_id": "p001",
                    "cantidad": 1
                }
            ]
        }
        response = self.client.post('/pedidos/', json=order_data)
        self.assertEqual(response.get_json()['DATA']['total'], 50.0)

        # Test descuento premium (10%)
        order_data['tipo_cliente'] = 'premium'
        response = self.client.post('/pedidos/', json=order_data)
        self.assertEqual(response.get_json()['DATA']['total'], 45.0)

        # Test descuento VIP (20%)
        order_data['tipo_cliente'] = 'VIP'
        response = self.client.post('/pedidos/', json=order_data)
        self.assertEqual(response.get_json()['DATA']['total'], 40.0)

if __name__ == '__main__':
    unittest.main()