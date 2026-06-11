from mi_api.Vendedor.domain.product_domain import Product
from mi_api.shared_store import PRODUCTS
from typing import Dict, List, Optional


class ProductRepository:

    def save(self, merchant_id: str, product: Product) -> Product:
        if merchant_id not in PRODUCTS:
            PRODUCTS[merchant_id] = {}
        PRODUCTS[merchant_id][product.product_id] = {
            "product_id": product.product_id,
            "merchant_id": merchant_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "available": product.available,
            "category": product.category,
            "photo_url": getattr(product, "photo_url", None),
        }
        return product

    def get_by_id(self, merchant_id: str, product_id: str) -> Optional[Product]:
        data = PRODUCTS.get(merchant_id, {}).get(product_id)
        if not data:
            return None
        return self._to_product(data)

    def get_all(self, merchant_id: str) -> List[Product]:
        return [self._to_product(p) for p in PRODUCTS.get(merchant_id, {}).values()]

    def update(self, merchant_id: str, product_id: str, updated_product: Product) -> Optional[Product]:
        if merchant_id in PRODUCTS and product_id in PRODUCTS[merchant_id]:
            updated_product.product_id = product_id
            self.save(merchant_id, updated_product)
            return updated_product
        return None

    def delete(self, merchant_id: str, product_id: str) -> bool:
        merchant_store = PRODUCTS.get(merchant_id, {})
        if product_id in merchant_store:
            del merchant_store[product_id]
            return True
        return False

    @staticmethod
    def _to_product(data: dict) -> Product:
        p = Product(
            name=data["name"],
            price=data["price"],
            stock=data.get("stock", 0),
            description=data.get("description"),
            category=data.get("category", "general"),
        )
        p.product_id = data["product_id"]
        p.available = data.get("available", p.stock > 0)
        return p
