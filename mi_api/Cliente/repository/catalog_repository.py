from mi_api.shared_store import MERCHANTS, PRODUCTS


class CatalogRepository:

    def get_merchant_by_id(self, merchant_id: str):
        m = MERCHANTS.get(merchant_id)
        if not m:
            return None
        return {
            "merchant_id": m["merchant_id"],
            "merchant_name": m["name"],
            "status": m["status"],
        }

    def get_products_by_merchant(self, merchant_id: str) -> list:
        return list(PRODUCTS.get(merchant_id, {}).values())
