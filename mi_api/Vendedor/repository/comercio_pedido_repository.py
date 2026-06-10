from typing import List, Optional
from domain.comercio_pedido_domain import OrderStatus, OrderSummary, ProductSummary
from repository.shared_store import MERCHANTS, ORDERS


class MerchantOrderRepository:

    def merchant_exists(self, merchant_id: str) -> bool:
        return merchant_id in MERCHANTS

    def get_orders(
        self,
        merchant_id: str,
        status_filter: Optional[OrderStatus] = None,
    ) -> List[OrderSummary]:
        orders = [o for o in ORDERS.values() if o["merchant_id"] == merchant_id]
        if status_filter is not None:
            orders = [o for o in orders if o["status"] == status_filter.value]
        orders.sort(key=lambda o: o["created_at"], reverse=True)
        return [self._hydrate(o) for o in orders]

    def _hydrate(self, data: dict) -> OrderSummary:
        return OrderSummary(
            order_id=data["order_id"],
            customer=data["customer"],
            status=OrderStatus(data["status"]),
            total=data["total"],
            products=[
                ProductSummary(p["name"], p["quantity"])
                for p in data["products"]
            ],
            notes=data.get("notes"),
            created_at=data["created_at"],
        )


merchant_order_repository = MerchantOrderRepository()
