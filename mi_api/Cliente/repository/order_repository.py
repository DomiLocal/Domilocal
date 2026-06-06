from domain.order_domain import Order


class OrderRepository:

    def __init__(self):
        self._orders: list[Order] = []
        self._next_id = 1

    def generate_order_id(self) -> str:
        order_id = f"PED-{self._next_id:05d}"
        self._next_id += 1
        return order_id

    def create(self, order: Order) -> Order:
        self._orders.append(order)
        return order

    def get_all(self) -> list[Order]:
        return self._orders.copy()


order_repository = OrderRepository()