from domain.product_domain import Product
from typing import List, Optional

class ProductRepository:
    def __init__(self):
        # In-memory database: {product_id: Product}
        self._db: dict[str, Product] = {}

    def save(self, product: Product) -> Product:
        self._db[product.product_id] = product
        return product

    def get_by_id(self, product_id: str) -> Optional[Product]:
        return self._db.get(product_id)

    def get_all(self) -> List[Product]:
        return list(self._db.values())

    def update(self, product_id: str, updated_product: Product) -> Optional[Product]:
        if product_id in self._db:
            updated_product.product_id = product_id
            self._db[product_id] = updated_product
            return updated_product
        return None

    def delete(self, product_id: str) -> bool:
        if product_id in self._db:
            del self._db[product_id]
            return True
        return False