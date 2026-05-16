from typing import List, Optional
from domain.models import Product

class ProductRepository:
    def __init__(self):
        self._products: List[Product] = []
        self._next_id = 1

    def get_all(self) -> List[Product]:
        return self._products

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return next((p for p in self._products if p.id == product_id), None)

    def create(self, product: Product) -> Product:
        product.id = self._next_id
        self._products.append(product)
        self._next_id += 1
        return product

# Singleton instance for demo purposes
product_repo = ProductRepository()
