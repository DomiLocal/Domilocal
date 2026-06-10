# ─────────────────────────────────────
# REPOSITORY LAYER
# In-memory catalog database
# ─────────────────────────────────────


class CatalogRepository:

    def __init__(self):

        self._merchants = [
            {
                "merchant_id": "COM-001",
                "merchant_name": "Tienda La Esquina",
                "status": "active"
            },
            {
                "merchant_id": "COM-002",
                "merchant_name": "Farmacia Central",
                "status": "active"
            },
            {
                "merchant_id": "COM-003",
                "merchant_name": "Market Closed",
                "status": "inactive"
            }
        ]

        self._products = [
            {
                "product_id": "P-001",
                "merchant_id": "COM-001",
                "name": "Agua 500ml",
                "description": "Agua mineral sin gas",
                "price": 1500,
                "stock": 20,
                "category": "bebidas",
                "photo_url": "https://domilocal.com/fotos/agua.jpg"
            },
            {
                "product_id": "P-002",
                "merchant_id": "COM-001",
                "name": "Gaseosa Cola",
                "description": "Bebida gaseosa",
                "price": 3500,
                "stock": 10,
                "category": "bebidas",
                "photo_url": "https://domilocal.com/fotos/gaseosa.jpg"
            },
            {
                "product_id": "P-003",
                "merchant_id": "COM-001",
                "name": "Pan Integral",
                "description": "Pan tajado integral",
                "price": 4200,
                "stock": 0,
                "category": "panaderia",
                "photo_url": None
            }
        ]

    def get_merchant_by_id(
        self,
        merchant_id: str
    ):

        return next(
            (
                merchant
                for merchant in self._merchants
                if merchant["merchant_id"] == merchant_id
            ),
            None
        )

    def get_products_by_merchant(
        self,
        merchant_id: str
    ):

        return [
            product
            for product in self._products
            if product["merchant_id"] == merchant_id
        ]