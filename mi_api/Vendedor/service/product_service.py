from typing import Dict, Any

from mi_api.Vendedor.domain.product_domain import ProductCreate, Product
from mi_api.Vendedor.repository.product_repository import ProductRepository
from mi_api.shared_store import MERCHANTS


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repo = repository

    def _validate_merchant(self, merchant_id: str):
        merchant = MERCHANTS.get(merchant_id)
        if not merchant:
            raise LookupError("Merchant not found.")
        if merchant["status"] == "inactive":
            raise ValueError("This business is currently unavailable.")
        if merchant["status"] != "active":
            raise ValueError("Merchant is not active.")

    def add_product(self, merchant_id: str, product_data: ProductCreate) -> Dict[str, Any]:
        self._validate_merchant(merchant_id)
        new_product = Product(**product_data.model_dump())
        new_product.update_availability()
        self.repo.save(merchant_id, new_product)

        message = (
            "Product added. Marked as unavailable due to zero stock."
            if not new_product.available
            else "Product added successfully to the catalog."
        )
        return {"message": message, "data": new_product.model_dump(), "success": True}

    def update_product(self, merchant_id: str, product_id: str, updated_data: ProductCreate) -> Dict[str, Any]:
        self._validate_merchant(merchant_id)
        existing_product = self.repo.get_by_id(merchant_id, product_id)
        if not existing_product:
            raise LookupError("Product not found.")

        existing_product.name = updated_data.name
        existing_product.price = updated_data.price
        existing_product.stock = updated_data.stock
        existing_product.description = updated_data.description
        existing_product.category = updated_data.category
        existing_product.update_availability()
        self.repo.update(merchant_id, product_id, existing_product)

        return {"message": "Product updated successfully.", "data": existing_product.model_dump(), "success": True}

    def delete_product(self, merchant_id: str, product_id: str) -> Dict[str, Any]:
        self._validate_merchant(merchant_id)
        if not self.repo.delete(merchant_id, product_id):
            raise LookupError("Product not found.")
        return {"message": "Product deleted successfully.", "success": True}
