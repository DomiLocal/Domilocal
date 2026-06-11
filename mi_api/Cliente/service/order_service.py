from datetime import datetime
from mi_api.Cliente.domain.order_domain import (
    OrderCreate,
    OrderCancellationRequest,
    Order,
)
from mi_api.Cliente.repository.order_repository import OrderRepository
from mi_api.Cliente.repository.client_repository import client_repository
from mi_api.shared_store import ORDERS, PRODUCTS


class OrderService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, order_data: OrderCreate):

        if not order_data.items:
            raise ValueError(
                "It is not possible to create an order with an empty cart."
            )

        if not order_data.delivery_address:
            raise ValueError("delivery_address is required.")

        store_ids = {item.store_id for item in order_data.items}

        if len(store_ids) > 1:
            raise ValueError(
                "You can only order products from one business per order."
            )

        store_id = next(iter(store_ids))

        # Validate each product exists in the merchant's catalog and is available
        for item in order_data.items:
            catalog = PRODUCTS.get(store_id, {})
            product = catalog.get(item.product_id)
            if not product:
                raise ValueError(
                    f"Product '{item.product_id}' is not available in this merchant's catalog."
                )
            if not product.get("available", False):
                raise ValueError(
                    f"Product '{product.get('name', item.product_id)}' is currently unavailable."
                )

        # Total is always calculated from catalog prices — client cannot manipulate it
        subtotal = sum(
            item.quantity * PRODUCTS[store_id][item.product_id]["price"]
            for item in order_data.items
        )
        delivery_fee = 3500
        total = subtotal + delivery_fee

        # Resolve customer identity if client_id is provided
        customer_name = "Cliente"
        customer_phone = None
        if order_data.client_id:
            client = client_repository.get_by_id(order_data.client_id)
            if client:
                customer_name = client.full_name
                customer_phone = client.phone

        order_id = self.repo.generate_order_id()

        order = Order(
            order_id=order_id,
            items=order_data.items,
            delivery_address=order_data.delivery_address,
            payment_method=order_data.payment_method,
            total=total,
            status="received",
            status_history=[
                {"status": "received", "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
            ],
        )

        self.repo.create(order)

        # Patch customer info into the shared store entry
        ORDERS[order_id]["customer"] = customer_name
        if customer_phone:
            ORDERS[order_id]["customer_phone"] = customer_phone

        return {
            "message": "Order created successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "total": order.total,
                "payment_method": order.payment_method,
                "delivery_address": order.delivery_address,
            },
            "success": True,
        }

    def cancel_order(self, order_id: str, cancellation_data: OrderCancellationRequest):

        order = self.repo.get_by_id(order_id)

        if not order:
            raise LookupError("Order not found.")

        if order.status in ["in_transit", "delivered"]:
            raise ValueError(
                "Unable to cancel the order. The dealer is already on the way."
            )

        if order.status not in ["received", "in_preparation"]:
            raise ValueError("Unable to cancel the order.")

        order.status = "cancelled"
        order.status_history.append(
            {"status": "cancelled", "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        )

        # Free dealer if one was assigned
        dealer_id = ORDERS.get(order_id, {}).get("dealer_id")
        if dealer_id:
            try:
                from mi_api.Repartidor.repository.dealer_repository import get_dealer_repository
                get_dealer_repository().update_availability(dealer_id, "available")
                print(f"[EVENT] Dealer {dealer_id} freed due to order {order_id} cancellation.")
            except Exception as e:
                print(f"[WARN] Could not free dealer on cancel: {e}")

        self.repo.save(order)

        return {
            "message": "Order cancelled successfully.",
            "data": {
                "order_id": order.order_id,
                "status": order.status,
                "reason": cancellation_data.reason,
            },
            "success": True,
        }
