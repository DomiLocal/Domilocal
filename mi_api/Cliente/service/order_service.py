from domain.order_domain import (
    OrderCreate,
    OrderCancellationRequest,
    Order
)

from repository.order_repository import OrderRepository


class OrderService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, order_data: OrderCreate):

        if not order_data.items:
            raise ValueError(
                "It is not possible to create an order with an empty cart."
            )

        if not order_data.delivery_address:
            raise ValueError(
                "delivery_address is required."
            )

        store_ids = {item.store_id for item in order_data.items}

        if len(store_ids) > 1:
            raise ValueError(
                "You can only order products from one business per order."
            )

        subtotal = sum(
            item.quantity * item.unit_price
            for item in order_data.items
        )

        delivery_fee = 3500

        total = subtotal + delivery_fee

        order_id = self.repo.generate_order_id()

        order = Order(
            order_id=order_id,
            items=order_data.items,
            delivery_address=order_data.delivery_address,
            payment_method=order_data.payment_method,
            total=total,
            status="received"
        )

        self.repo.create(order)

        return {
            "message": "Order created successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "total": order.total,
                "payment_method": order.payment_method,
                "delivery_address": order.delivery_address
            },
            "success": True
        }

    def cancel_order(
        self,
        order_id: str,
        cancellation_data: OrderCancellationRequest
    ):

        order = self.repo.get_by_id(order_id)

        if not order:
            raise LookupError(
                "Order not found."
            )

        if order.status in [
            "in_transit",
            "delivered"
        ]:
            raise ValueError(
                "Unable to cancel the order. The driver is already on the way."
            )

        if order.status not in [
            "received",
            "in_preparation"
        ]:
            raise ValueError(
                "Unable to cancel the order."
            )

        order.status = "cancelled"

        return {
            "message": "Order cancelled successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "reason": cancellation_data.reason
            },
            "success": True
        }