# ─────────────────────────────────────────────────────────────
# SERVICE — consulta_pedidos
# Handles business logic for retrieving orders for a commerce.
# Validates existence of commerce and applies rules/filters.
# ─────────────────────────────────────────────────────────────

from typing import Dict, Any, Optional
from repository.comercio_pedido_repository import MerchantOrderRepository, merchant_order_repository
from domain.comercio_pedido_domain import OrderStatus


class MerchantOrderService:

    def __init__(self, repository: MerchantOrderRepository):
        self.repository = repository

    def get_merchant_orders(
        self,
        merchant_id: str,
        status_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves orders for a given merchant ID.
        Checks for merchant existence, else raises LookupError (404).
        """
        # Case 4 - ID de comercio inexistente
        if not self.repository.merchant_exists(merchant_id):
            raise LookupError(f"Merchant {merchant_id} not found.")

        # Convert status filter string to OrderStatus enum if passed
        parsed_status = None
        if status_filter:
            try:
                # Find matching enum value
                parsed_status = OrderStatus(status_filter)
            except ValueError:
                # If the status is not valid, we can raise ValueError to return HTTP 400
                raise ValueError(f"Invalid status filter: {status_filter}")

        orders_list = self.repository.get_orders(merchant_id, parsed_status)

        # Build response structure specified in the JSON example
        return {
            "message": "Orders retrieved successfully.",
            "data": {
                "merchant_id": merchant_id,
                "total_orders": len(orders_list),
                "orders": [order.to_dict() for order in orders_list]
            },
            "success": True
        }


merchant_order_service = MerchantOrderService(merchant_order_repository)
