from datetime import datetime
from typing import Dict, Any, Optional

from mi_api.Vendedor.repository.comercio_pedido_repository import MerchantOrderRepository, merchant_order_repository
from mi_api.Vendedor.domain.comercio_pedido_domain import OrderStatus
from mi_api.shared_store import ORDERS


class MerchantOrderService:

    def __init__(self, repository: MerchantOrderRepository):
        self.repository = repository

    def get_merchant_orders(self, merchant_id: str, status_filter: Optional[str] = None) -> Dict[str, Any]:
        if not self.repository.merchant_exists(merchant_id):
            raise LookupError(f"Merchant {merchant_id} not found.")

        parsed_status = None
        if status_filter:
            try:
                parsed_status = OrderStatus(status_filter)
            except ValueError:
                raise ValueError(f"Invalid status filter: {status_filter}")

        orders_list = self.repository.get_orders(merchant_id, parsed_status)

        return {
            "message": "Orders retrieved successfully.",
            "data": {
                "merchant_id": merchant_id,
                "total_orders": len(orders_list),
                "orders": [order.to_dict() for order in orders_list],
            },
            "success": True,
        }


    def toggle_order_status(self, merchant_id: str, order_id: str) -> Dict[str, Any]:
        if not self.repository.merchant_exists(merchant_id):
            raise LookupError(f"Merchant {merchant_id} not found.")
        order_data = ORDERS.get(order_id)
        if not order_data or order_data.get("merchant_id") != merchant_id:
            raise LookupError(f"Order {order_id} not found for merchant {merchant_id}.")
        toggle_map = {
            "received": "in_preparation",
            "in_preparation": "received",
        }
        current = order_data["status"]
        if current not in toggle_map:
            raise ValueError(
                f"Cannot toggle order in '{current}' status. "
                "Only 'received' ↔ 'in_preparation' can be toggled here."
            )
        new_status = toggle_map[current]
        ORDERS[order_id]["status"] = new_status
        ORDERS[order_id]["updated_at"] = datetime.utcnow()
        ORDERS[order_id].setdefault("status_history", []).append(
            {"status": new_status, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        )
        return {
            "message": f"Order status changed to '{new_status}'.",
            "data": {"order_id": order_id, "merchant_id": merchant_id, "status": new_status},
            "success": True,
        }


merchant_order_service = MerchantOrderService(merchant_order_repository)
