from mi_api.Cliente.domain.catalog_domain import (
    CatalogProductResponse,
    CatalogDataResponse,
    CatalogResponse,
)
from mi_api.Cliente.repository.catalog_repository import CatalogRepository


class CatalogService:

    def __init__(self, repository: CatalogRepository):
        self.repository = repository

    def get_catalog(
        self,
        merchant_id: str,
        category: str | None = None,
        search: str | None = None,
    ):
        merchant = self.repository.get_merchant_by_id(merchant_id)

        if not merchant:
            raise ValueError("Merchant not found.")

        if merchant["status"] != "active":
            raise ValueError("Merchant not found.")

        products = self.repository.get_products_by_merchant(merchant_id)

        # Hide products with stock = 0
        products = [p for p in products if p["stock"] > 0]

        if category:
            products = [p for p in products if p["category"].lower() == category.lower()]

        if search:
            products = [p for p in products if search.lower() in p["name"].lower()]

        catalog_products = [
            CatalogProductResponse(
                product_id=p["product_id"],
                name=p["name"],
                description=p["description"],
                price=p["price"],
                stock=p["stock"],
                category=p["category"],
                photo_url=p["photo_url"],
            )
            for p in products
        ]

        return CatalogResponse(
            message="Catalog retrieved successfully.",
            data=CatalogDataResponse(
                merchant_id=merchant["merchant_id"],
                merchant_name=merchant["merchant_name"],
                products=catalog_products,
            ),
            success=True,
        )
