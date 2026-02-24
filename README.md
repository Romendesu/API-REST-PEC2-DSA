# API REST de Gestión de Productos y Pedidos

Una API REST completa para la gestión de productos y pedidos, implementada con Python y Flask, utilizando diversos patrones de diseño para una arquitectura robusta y mantenible.

## 📋 Descripción

Esta API permite gestionar un catálogo de productos y procesar pedidos con funcionalidades avanzadas como descuentos automáticos, notificaciones en tiempo real, procesamiento de pagos y exportación de datos. Está diseñada siguiendo los principios SOLID y utilizando patrones de diseño reconocidos.

## 🎯 Requisitos Funcionales

### Gestión de Productos
- ✅ Registrar productos con nombre, precio y categoría
- ✅ Listar todos los productos disponibles

### Gestión de Pedidos
- ✅ Crear pedidos asociando productos y cantidades
- ✅ Aplicar descuentos según tipo de cliente (normal: 0%, premium: 10%, VIP: 20%)
- ✅ Cambiar estado del pedido: PENDIENTE → PROCESANDO → ENVIADO → ENTREGADO
- ✅ Cancelar pedidos (solo si están en estado PENDIENTE)

### Notificaciones
- ✅ Notificar automáticamente a cliente, almacén y facturación al cambiar estado

### Métodos de Pago
- ✅ Soporte para tarjeta de crédito, PayPal y transferencia bancaria
- ✅ Procesamiento automático al confirmar pedido

### Exportación
- ✅ Exportar detalles de pedidos en formato JSON o texto plano

## 🏗️ Patrones de Diseño Implementados

| Patrón | Tipo | Aplicación |
|--------|------|------------|
| **Singleton** | Creacional | Base de datos en memoria (repositorio único) |
| **Factory Method** | Creacional | Creación de métodos de pago |
| **Builder** | Creacional | Construcción de objetos Pedido complejos |
| **Observer** | Comportamiento | Notificaciones al cambiar estado del pedido |
| **State** | Comportamiento | Ciclo de vida y estados del pedido |
| **Strategy** | Comportamiento | Cálculo de descuentos según tipo de cliente |
| **Decorator** | Estructural | Exportación del pedido en distintos formatos |

## 📁 Estructura del Proyecto

```
API-REST-PEC2-DSA-main/
├── main.py                 # Punto de entrada de la aplicación
├── test_api.py            # Archivo de pruebas unitarias
├── requirements.txt       # Dependencias del proyecto
├── database/
│   ├── __init__.py
│   └── database.py        # Implementación de la base de datos (Singleton)
├── orders/
│   ├── __init__.py
│   ├── order.py           # Clase Order con Observer y State
│   ├── routes.py          # Endpoints de pedidos
│   ├── create_orders.py   # Builder para pedidos
│   ├── observer.py        # Implementación Observer
│   ├── state.py           # Implementación State
│   ├── discount_strategy.py # Strategy para descuentos
│   └── export_decorator.py # Decorator para exportación
├── products/
│   ├── __init__.py
│   └── routes.py          # Endpoints de productos
└── utils/
    ├── __init__.py
    ├── constants.py       # Constantes HTTP
    ├── response.py        # Factory para respuestas
    └── payment_factory.py # Factory Method para pagos
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.10+
- pip

### Instalación
1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd API-REST-PEC2-DSA-main
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

La API estará disponible en `http://127.0.0.1:5000`

## 📡 Endpoints de la API

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos` | Listar todos los productos |
| POST | `/productos` | Crear un nuevo producto |

### Pedidos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/pedidos` | Listar todos los pedidos |
| POST | `/pedidos` | Crear un nuevo pedido |
| GET | `/pedidos/<id>` | Obtener detalle de un pedido |
| PUT | `/pedidos/<id>/avanzar` | Avanzar al siguiente estado |
| PUT | `/pedidos/<id>/cancelar` | Cancelar pedido pendiente |
| GET | `/pedidos/<id>/exportar?formato=json` | Exportar pedido (json/texto) |

## 📝 Ejemplos de Uso

### Crear un Producto
```bash
POST /productos
Content-Type: application/json

{
  "nombre": "Laptop Gaming",
  "precio": 1200.50,
  "categoria": "Electrónica"
}
```

### Crear un Pedido
```bash
POST /pedidos
Content-Type: application/json

{
  "cliente": "Juan Pérez",
  "tipo_cliente": "premium",
  "metodo_pago": "PayPal",
  "items": [
    {
      "producto_id": "p0",
      "cantidad": 1
    }
  ]
}
```

### Avanzar Estado de Pedido
```bash
PUT /pedidos/p0/avanzar
```

### Exportar Pedido en JSON
```bash
GET /pedidos/p0/exportar?formato=json
```

## 🧪 Ejecutar Pruebas

```bash
python test_api.py
```

O con pytest (si está instalado):
```bash
pytest test_api.py -v
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje de programación
- **Flask 3.x**: Framework web para la API REST
- **Flask-CORS**: Manejo de CORS
- **Unittest**: Framework de pruebas

## 📊 Características Técnicas

- **Base de datos**: En memoria (no persistente entre sesiones)
- **Arquitectura**: Modular con separación de responsabilidades
- **Patrones**: 7 patrones de diseño implementados
- **Respuestas**: JSON estandarizado con códigos HTTP apropiados
- **Validación**: Validación de datos en endpoints
- **Notificaciones**: Sistema de observadores para cambios de estado

## 🎯 Estados del Pedido

```
PENDIENTE → PROCESANDO → ENVIADO → ENTREGADO
    ↓
CANCELADO (solo desde PENDIENTE)
```

## 💰 Sistema de Descuentos

- **Normal**: 0% descuento
- **Premium**: 10% descuento
- **VIP**: 20% descuento

Los descuentos se aplican automáticamente al subtotal del pedido.

## 🔧 Configuración

La aplicación utiliza configuración por defecto de Flask. Para entornos de producción, considera configurar variables de entorno para:
- `FLASK_ENV=production`
- `FLASK_DEBUG=false`

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte o preguntas, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando patrones de diseño y buenas prácticas de desarrollo.**