/*

Prueba 2: GET /pedidos/<id>/exportar?formato=json
Esta ruta exporta los detalles del pedido en formato JSON.

*/ 


// PASO 1: Crear producto
fetch('http://127.0.0.1:5000/productos/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "nombre": "Monitor 4K",
    "precio": 300.00,
    "categoria": "Monitores"
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
      "cliente": "Carlos Ruiz",
      "tipo_cliente": "VIP", // 20% descuento
      "metodo_pago": "tarjeta de crédito",
      "items": [{
        "producto_id": productData.DATA.id,
        "cantidad": 1
      }]
    })
  });
})
.then(res => res.json())
.then(orderData => {
  console.log('Pedido creado con descuento aplicado');
  
  // PASO 3: Exportar pedido en JSON
  const orderId = orderData.DATA.id;
  return fetch(`http://127.0.0.1:5000/pedidos/${orderId}/exportar?formato=json`);
})
.then(res => res.json())
.then(exportData => {
  console.log('✅ Exportación exitosa');
  const pedido = JSON.parse(exportData.DATA);
  console.log('Datos del pedido:', pedido);
  console.log('Cliente:', pedido.cliente);
  console.log('Estado:', pedido.estado);
  console.log('Total con descuento:', pedido.total);
})
.catch(error => console.error('❌ Error:', error));