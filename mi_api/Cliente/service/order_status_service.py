from repository.order_repository import OrderRepository


class OrderStatusService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def get_order_status(self, order_id: str):

        order = self.repo.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found.")

        return {
            "message": "Order status retrieved successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "driver": None,
                "status_history": [
                    {
                        "status": order.status,
                        "time": "2026-06-09T20:00:00Z"
                    }
                ]
            },
            "success": True
        }