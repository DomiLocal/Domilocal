import logging
import urllib.request
from repository.order_repository import OrderRepository, DatabaseConnectionError

logger = logging.getLogger("order_service")


class OrderService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def mark_order_as_ready(self, order_id: str) -> dict:
        # 1. Retrieve the order (handles 503/404)
        order = self.repo.get_by_id(order_id)
        if order is None:
            raise KeyError(f"Order with ID {order_id} does not exist.")

        # 2. Transition state (handles 400 if not in_preparation)
        order.mark_as_ready_for_pickup()

        # 3. Persist the state change
        self.repo.save(order)

        # 4. Notify modules (best-effort, non-blocking)
        self._notify_delivery_module(order_id)
        self._notify_client(order_id)

        return {
            "message": "Order marked as ready for pickup.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "updated_at": order.updated_at
            },
            "success": True
        }

    def _notify_delivery_module(self, order_id: str):
        """
        Notifies the courier / delivery assignment module via HTTP POST.
        Uses stdlib urllib — no extra packages required.
        """
        url = f"http://localhost:8000/api/v1/pedidos/{order_id}/asignar-repartidor"
        logger.info(f"Notifying delivery module for order {order_id} ...")
        try:
            req = urllib.request.Request(url, method="POST")
            with urllib.request.urlopen(req, timeout=1) as resp:
                logger.info(f"Delivery module response: {resp.status}")
        except Exception as e:
            logger.warning(f"Could not reach delivery assignment module: {e}")

    def _notify_client(self, order_id: str):
        """
        Notifies the client.
        """
        logger.info(f"Client notified: Order {order_id} is ready for pickup!")
