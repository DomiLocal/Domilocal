from datetime import datetime, timedelta
from domain.order_domain import Order


now = datetime.utcnow()


def _ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class OrderRepository:

    def __init__(self):
        self._next_id = 3

        # Pre-seeded orders for testing
        self._orders: list[Order] = [
            Order(
                order_id="PED-00001",
                items=[
                    {"product_name": "Agua 500ml", "store_id": "COM-001", "quantity": 2, "unit_price": 1500}
                ],
                delivery_address="Calle 5 # 10-20, Bucaramanga",
                payment_method="cash",
                total=6500.0,
                status="in_transit",
                dealer={"name": "Carlos Pérez", "phone": "3009876543"},
                status_history=[
                    {"status": "received",       "time": _ts(now - timedelta(hours=1))},
                    {"status": "in_preparation", "time": _ts(now - timedelta(minutes=40))},
                    {"status": "in_transit",     "time": _ts(now - timedelta(minutes=15))},
                ]
            ),
            Order(
                order_id="PED-00002",
                items=[
                    {"product_name": "Gaseosa Cola", "store_id": "COM-001", "quantity": 1, "unit_price": 3500}
                ],
                delivery_address="Carrera 10 # 5-30, Bucaramanga",
                payment_method="online_payment",
                total=7000.0,
                status="received",
                status_history=[
                    {"status": "received", "time": _ts(now - timedelta(minutes=5))},
                ]
            ),
        ]

    def generate_order_id(self) -> str:
        order_id = f"PED-{self._next_id:05d}"
        self._next_id += 1
        return order_id

    def create(self, order: Order) -> Order:
        self._orders.append(order)
        return order

    def get_all(self) -> list[Order]:
        return self._orders.copy()

    def get_by_id(self, order_id: str):
        return next(
            (order for order in self._orders if order.order_id == order_id),
            None
        )


order_repository = OrderRepository()
