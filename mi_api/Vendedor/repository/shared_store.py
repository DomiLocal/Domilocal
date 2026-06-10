from datetime import datetime, timedelta

now = datetime.utcnow()

# Single source of truth for merchants.
# Both ComercioRepository and MerchantOrderRepository read/write here.
MERCHANTS: dict = {
    "COM-001": {
        "merchant_id": "COM-001",
        "name": "Tienda La Esquina",
        "address": "Calle 5 # 10-20, Bucaramanga",
        "category": "tienda_de_barrio",
        "phone": "3001234567",
        "email": "laesquina@gmail.com",
        "status": "active",
    },
    "COM-002": {
        "merchant_id": "COM-002",
        "name": "Restaurante El Buen Sabor",
        "address": "Carrera 15 # 8-45, Bucaramanga",
        "category": "restaurante",
        "phone": "3009876543",
        "email": "buensabor@gmail.com",
        "status": "active",
    },
}

# Single source of truth for orders.
# Both RepositorioPedido and MerchantOrderRepository read/write here.
# Mutations by one repository are immediately visible to the other.
ORDERS: dict = {
    "PED-0789": {
        "order_id": "PED-0789",
        "merchant_id": "COM-001",
        "customer": "Ana Gómez",
        "status": "in_preparation",
        "total": 18500.0,
        "products": [
            {"name": "Agua 500ml", "quantity": 2},
            {"name": "Pan tajado", "quantity": 1},
        ],
        "notes": "Sin sal por favor",
        "created_at": now - timedelta(minutes=5),
        "updated_at": None,
    },
    "PED-0790": {
        "order_id": "PED-0790",
        "merchant_id": "COM-001",
        "customer": "Carlos Ríos",
        "status": "received",
        "total": 32000.0,
        "products": [
            {"name": "Jugo de naranja", "quantity": 1},
            {"name": "Sándwich pollo", "quantity": 2},
        ],
        "notes": None,
        "created_at": now - timedelta(minutes=20),
        "updated_at": None,
    },
    "PED-0788": {
        "order_id": "PED-0788",
        "merchant_id": "COM-001",
        "customer": "Luisa Martínez",
        "status": "ready_for_pickup",
        "total": 9500.0,
        "products": [
            {"name": "Café americano", "quantity": 1},
        ],
        "notes": "Extra caliente",
        "created_at": now - timedelta(hours=1),
        "updated_at": None,
    },
    "PED-0787": {
        "order_id": "PED-0787",
        "merchant_id": "COM-001",
        "customer": "Pedro Vargas",
        "status": "delivered",
        "total": 45000.0,
        "products": [
            {"name": "Almuerzo ejecutivo", "quantity": 3},
            {"name": "Agua 1.5L", "quantity": 3},
        ],
        "notes": None,
        "created_at": now - timedelta(hours=3),
        "updated_at": None,
    },
    "PED-0786": {
        "order_id": "PED-0786",
        "merchant_id": "COM-001",
        "customer": "María Suárez",
        "status": "cancelled",
        "total": 12000.0,
        "products": [
            {"name": "Torta de chocolate", "quantity": 1},
        ],
        "notes": "Cambié de opinión",
        "created_at": now - timedelta(hours=5),
        "updated_at": None,
    },
}
