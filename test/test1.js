/*Prueba 1: PUT /pedidos/<id>/cancelar*/


// PASO 1: Crear producto
fetch('http://127.0.0.1:5000/productos/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "nombre": "Teclado Mecánico",
    "precio": 100.00,
    "categoria": "Accesorios"
  })
})
.then(res => res.json())
.then(productData => {
  console.log('Producto creado:', productData.DATA.id);
  
  // PASO 2: Crear pedido
  return fetch('http://127.0.0.1:5000/pedidos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      "cliente": "María López",
      "tipo_cliente": "normal",
      "metodo_pago": "transferencia bancaria",
      "items": [{
        "producto_id": productData.DATA.id,
        "cantidad": 1
      }]
    })
  });
})
.then(res => res.json())
.then(orderData => {
  console.log('Pedido creado en estado:', orderData.DATA.estado); // PENDIENTE
  
  // PASO 3: Cancelar pedido
  const orderId = orderData.DATA.id;
  return fetch(`http://127.0.0.1:5000/pedidos/${orderId}/cancelar`, {
    method: 'PUT'
  });
})
.then(res => res.json())
.then(cancelData => {
  console.log('✅ Pedido cancelado exitosamente');
  console.log('Nuevo estado:', cancelData.DATA.estado); // CANCELADO
  console.log('Notificaciones enviadas a: Cliente, Almacén, Facturación');
})
.catch(error => console.error('❌ Error:', error));