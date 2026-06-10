from repository.order_repository import OrderRepository


class OrderStatusService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def get_order_status(self, order_id: str):

        order = self.repo.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found.")

        dealer = order.dealer if order.status == "in_transit" else None

        return {
            "message": "Order status retrieved successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "dealer": dealer,
                "status_history": order.status_history
            },
            "success": True
        }
