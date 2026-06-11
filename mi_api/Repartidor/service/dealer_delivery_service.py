from datetime import datetime, timezone

from mi_api.Repartidor.domain.dealer_delivery_domain import DeliveryConfirmationResponseData
from mi_api.Repartidor.repository.dealer_repository import DealerRepository
from mi_api.shared_store import ORDERS, PRODUCTS


class DealerDeliveryService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def confirm_delivery(self, order_id: str) -> DeliveryConfirmationResponseData:
        order = self.repo.find_order_by_id(order_id)
        if not order:
            raise LookupError("Order not found.")

        if order.status != "in_transit":
            raise ValueError("Unable to confirm delivery. The order is not in transit.")

        delivery_time = datetime.now(timezone.utc)
        self.repo.update_order_status(order_id, "delivered", delivery_time)
        self._reduce_stock(order_id)

        if order.dealer_id:
            self.repo.update_availability(order.dealer_id, "available")
            print(f"[NOTIFICATION] Dealer {order.dealer_id} is now available.")

        print(f"[NOTIFICATION] Client notified: Order {order_id} has been delivered.")
        print(f"[NOTIFICATION] Store notified: Delivery of order {order_id} confirmed successfully.")

        delivery_time_str = delivery_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return DeliveryConfirmationResponseData(
            order_id=order_id,
            status="delivered",
            delivery_time=delivery_time_str,
            driver_status="available",
        )

    def _reduce_stock(self, order_id: str) -> None:
        order_data = ORDERS.get(order_id, {})
        store_id = order_data.get("merchant_id", "")
        catalog = PRODUCTS.get(store_id, {})
        for item in order_data.get("items", []):
            product_id = item.get("product_id")
            if product_id and product_id in catalog:
                catalog[product_id]["stock"] = max(0, catalog[product_id]["stock"] - item.get("quantity", 1))
                if catalog[product_id]["stock"] == 0:
                    catalog[product_id]["available"] = False
