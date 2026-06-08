from repository.product_repository import ProductRepository
from domain.product_domain import ProductCreate, Product
from typing import Dict, Any

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repo = repository

    def add_product(self, product_data: ProductCreate) -> Dict[str, Any]:
        # Rule: if stock is 0, available=False
        new_product = Product(**product_data.model_dump())
        new_product.update_availability()

        self.repo.save(new_product)

        message = (
            "Product added. Marked as unavailable because stock is 0."
            if not new_product.available
            else "Product added successfully to the catalog."
        )
        return {
            "message": message,
            "data": new_product.model_dump(),
            "success": True
        }

    def update_product(self, merchant_id: str, product_id: str, updated_data: ProductCreate) -> Dict[str, Any]:
        existing_product = self.repo.get_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        existing_product.name = updated_data.name
        existing_product.price = updated_data.price
        existing_product.stock = updated_data.stock
        existing_product.description = updated_data.description
        existing_product.update_availability()

        self.repo.update(product_id, existing_product)
        return {
            "message": "Product updated successfully",
            "data": existing_product.model_dump(),
            "success": True
        }

    def delete_product(self, merchant_id: str, product_id: str) -> Dict[str, Any]:
        if not self.repo.delete(product_id):
            raise ValueError("Product not found")
        return {"message": "Product deleted", "success": True}