# ─────────────────────────────────────
# SERVICE LAYER
# Catalog business logic
# ─────────────────────────────────────

from domain.catalog_domain import (
    CatalogProductResponse,
    CatalogDataResponse,
    CatalogResponse
)

from repository.catalog_repository import (
    CatalogRepository
)


class CatalogService:

    def __init__(
        self,
        repository: CatalogRepository
    ):
        self.repository = repository

    def get_catalog(
        self,
        merchant_id: str,
        category: str | None = None,
        search: str | None = None
    ):

        # ── Rule 1: Merchant must exist ─────────────────────

        merchant = self.repository.get_merchant_by_id(
            merchant_id
        )

        if not merchant:

            raise ValueError(
                "Merchant not found."
            )

        # ── Rule 2: Merchant must be active ────────────────

        if merchant["status"] != "active":

            raise ValueError(
                "Merchant not found."
            )

        products = self.repository.get_products_by_merchant(
            merchant_id
        )

        # ── Rule 3: Hide products with stock = 0 ───────────

        products = [
            product
            for product in products
            if product["stock"] > 0
        ]

        # ── Rule 4: Filter by category ─────────────────────

        if category:

            products = [
                product
                for product in products
                if product["category"].lower() == category.lower()
            ]

        # ── Rule 5: Search by product name ─────────────────

        if search:

            products = [
                product
                for product in products
                if search.lower() in product["name"].lower()
            ]

        catalog_products = [

            CatalogProductResponse(
                product_id=product["product_id"],
                name=product["name"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"],
                category=product["category"],
                photo_url=product["photo_url"]
            )

            for product in products
        ]

        return CatalogResponse(

            message="Catalog retrieved successfully.",

            data=CatalogDataResponse(
                merchant_id=merchant["merchant_id"],
                merchant_name=merchant["merchant_name"],
                products=catalog_products
            ),

            success=True
        )