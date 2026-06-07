# ─────────────────────────────────────────────────────────────
# CAPA SERVICIO (HU-C03) — Repartidor/service/dealer_delivery_service.py
# ─────────────────────────────────────────────────────────────
from datetime import datetime, timezone
from domain.dealer_delivery_domain import DeliveryConfirmationResponseData
from repository.dealer_repository import DealerRepository


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

        if order.dealer_id:
            self.repo.update_availability(order.dealer_id, "available")
            print(f"[NOTIFICATION] Dealer {order.dealer_id} is now available.")

        # Notificaciones al cliente y al comercio
        print(f"[NOTIFICATION] Client notified: Order {order_id} has been delivered.")
        print(f"[NOTIFICATION] Store notified: Delivery of order {order_id} confirmed successfully.")

        delivery_time_str = delivery_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return DeliveryConfirmationResponseData(
            order_id=order_id,
            status="delivered",
            delivery_time=delivery_time_str,
            driver_status="available"
        )
