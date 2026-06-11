from datetime import datetime
from mi_api.shared_store import ORDERS, next_order_id
from mi_api.Cliente.domain.order_domain import Order


class OrderRepository:

    def generate_order_id(self) -> str:
        return next_order_id()

    def create(self, order: Order) -> Order:
        items_raw = [
            item.model_dump() if hasattr(item, "model_dump") else dict(item)
            for item in order.items
        ]
        products = [
            {"name": it.get("product_name", ""), "quantity": it.get("quantity", 1)}
            for it in items_raw
        ]
        merchant_id = items_raw[0]["store_id"] if items_raw else ""

        ORDERS[order.order_id] = {
            "order_id": order.order_id,
            "merchant_id": merchant_id,
            "customer": "Cliente",
            "client_id": None,
            "status": order.status,
            "total": order.total,
            "items": items_raw,
            "products": products,
            "delivery_address": order.delivery_address,
            "payment_method": order.payment_method,
            "dealer_id": None,
            "dealer": None,
            "notes": None,
            "status_history": order.status_history,
            "created_at": datetime.utcnow(),
            "updated_at": None,
            "delivery_time": None,
        }
        return order

    def get_all(self) -> list[Order]:
        return [self._to_order(v) for v in ORDERS.values()]

    def get_by_id(self, order_id: str):
        data = ORDERS.get(order_id)
        if not data:
            return None
        return self._to_order(data)

    def save(self, order: Order) -> Order:
        if order.order_id in ORDERS:
            ORDERS[order.order_id]["status"] = order.status
            ORDERS[order.order_id]["status_history"] = order.status_history
            ORDERS[order.order_id]["updated_at"] = datetime.utcnow()
            if order.dealer:
                ORDERS[order.order_id]["dealer"] = order.dealer
        return order

    @staticmethod
    def _to_order(data: dict) -> Order:
        return Order(
            order_id=data["order_id"],
            items=data.get("items", []),
            delivery_address=data.get("delivery_address", ""),
            payment_method=data.get("payment_method", "cash"),
            total=data.get("total", 0.0),
            status=data["status"],
            dealer=data.get("dealer"),
            status_history=data.get("status_history", []),
        )


order_repository = OrderRepository()
