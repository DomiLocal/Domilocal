from typing import List, Optional
from domain.models import Product
from repository.product_repo import product_repo

class ProductService:
    def list_products(self) -> List[Product]:
        return product_repo.get_all()

    def get_product(self, product_id: int) -> Optional[Product]:
        return product_repo.get_by_id(product_id)

    def add_product(self, product: Product) -> Product:
        return product_repo.create(product)

product_service = ProductService()
