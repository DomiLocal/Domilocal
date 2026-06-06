from typing import Optional
from domain.order_domain import Order


class DatabaseConnectionError(Exception):
    """Exception raised when the simulated database is unavailable."""
    pass


class OrderRepository:

    def __init__(self):
        # Simulated database storage
        self._orders: dict[str, Order] = {
            "PED-00001": Order(order_id="PED-00001", status="in_preparation"),
            "PED-00002": Order(order_id="PED-00002", status="received"),
            "PED-00003": Order(order_id="PED-00003", status="ready_for_pickup"),
            "PED-0789": Order(order_id="PED-0789", status="in_preparation")
        }
        self._db_available: bool = True

    def set_db_availability(self, available: bool) -> None:
        self._db_available = available

    def get_by_id(self, order_id: str) -> Optional[Order]:
        if not self._db_available:
            raise DatabaseConnectionError("Database connection failed.")
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        if not self._db_available:
            raise DatabaseConnectionError("Database connection failed.")
        self._orders[order.order_id] = order


# Shared repository singleton instance
order_repository = OrderRepository()
