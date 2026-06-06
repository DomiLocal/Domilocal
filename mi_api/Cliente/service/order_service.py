from domain.order_domain import (
    OrderCreate,
    OrderResponse,
    Order
)

from repository.order_repository import OrderRepository


class OrderService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, order_data: OrderCreate):

        # Regla 1: carrito no vacío
        if not order_data.items:
            raise ValueError(
                "It is not possible to create an order with an empty cart."
            )

        # Regla 2: todos los productos deben ser del mismo comercio
        store_ids = {item.store_id for item in order_data.items}

        if len(store_ids) > 1:
            raise ValueError(
                "You can only order products from the same store in a single order."
            )

        # Calcular subtotal
        subtotal = sum(
            item.quantity * item.unit_price
            for item in order_data.items
        )

        # Costo fijo de envío
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