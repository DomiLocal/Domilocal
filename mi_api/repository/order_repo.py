from typing import List, Optional
from domain.models import Order, OrderStatus
from datetime import datetime

class OrderRepository:
    def __init__(self):
        self._orders: List[Order] = []
        self._counter = 1

    def create(self, order: Order) -> Order:
        order.id_pedido = f"PED-{self._counter:04d}"
        order.historial_estados = [{"estado": order.estado, "hora": datetime.now()}]
        self._orders.append(order)
        self._counter += 1
        return order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return next((o for o in self._orders if o.id_pedido == order_id), None)

    def get_by_vendor(self, vendor_id: str, status: Optional[OrderStatus] = None) -> List[Order]:
        orders = [o for o in self._orders if o.id_comercio == vendor_id]
        if status:
            orders = [o for o in orders if o.estado == status]
        return sorted(orders, key=lambda x: x.fecha_creacion, reverse=True)

    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        order = self.get_by_id(order_id)
        if order:
            order.estado = status
            order.historial_estados.append({"estado": status, "hora": datetime.now()})
            return order
        return None

    def get_active_by_delivery(self, dp_id: str) -> Optional[Order]:
        return next((o for o in self._orders if o.id_repartidor == dp_id and o.estado != OrderStatus.ENTREGADO and o.estado != OrderStatus.CANCELADO), None)

order_repo = OrderRepository()
