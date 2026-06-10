from domain.product_domain import Product
from typing import Dict, List, Optional


class ProductRepository:
    def __init__(self):
        # {merchant_id: {product_id: Product}}
        self._db: Dict[str, Dict[str, Product]] = {}

    def save(self, merchant_id: str, product: Product) -> Product:
        if merchant_id not in self._db:
            self._db[merchant_id] = {}
        self._db[merchant_id][product.product_id] = product
        return product

    def get_by_id(self, merchant_id: str, product_id: str) -> Optional[Product]:
        return self._db.get(merchant_id, {}).get(product_id)

    def get_all(self, merchant_id: str) -> List[Product]:
        return list(self._db.get(merchant_id, {}).values())

    def update(self, merchant_id: str, product_id: str, updated_product: Product) -> Optional[Product]:
        merchant_store = self._db.get(merchant_id, {})
        if product_id in merchant_store:
            updated_product.product_id = product_id
            merchant_store[product_id] = updated_product
            return updated_product
        return None

    def delete(self, merchant_id: str, product_id: str) -> bool:
        merchant_store = self._db.get(merchant_id, {})
        if product_id in merchant_store:
            del merchant_store[product_id]
            return True
        return False
