# ─────────────────────────────────────────────────────────────
# REPOSITORY — consulta_pedidos
# In-memory store that persists orders grouped by merchant id.
# Pre-seeded with realistic test data so the endpoint works
# immediately without any database.
# ─────────────────────────────────────────────────────────────

from typing import Dict, List, Optional
from datetime import datetime, timedelta

from domain.comercio_pedido_domain import (
    OrderStatus,
    OrderSummary,
    ProductSummary,
)


class MerchantOrderRepository:

    def __init__(self):
        # { merchant_id: [OrderSummary, ...] }
        # Orders are stored newest-first already (insertion order kept).
        self._store: Dict[str, List[OrderSummary]] = {}
        self._seed()

    # ── public interface ────────────────────────────────────────

    def merchant_exists(self, merchant_id: str) -> bool:
        return merchant_id in self._store

    def get_orders(
        self,
        merchant_id: str,
        status_filter: Optional[OrderStatus] = None,
    ) -> List[OrderSummary]:
        """
        Return orders for *merchant_id* sorted newest-first.
        Optionally filter by *status_filter*.
        """
        orders = self._store.get(merchant_id, [])

        if status_filter is not None:
            orders = [o for o in orders if o.status == status_filter]

        # newest first (highest created_at first)
        return sorted(orders, key=lambda o: o.created_at, reverse=True)

    # ── seeding ────────────────────────────────────────────────

    def _seed(self):
        now = datetime.utcnow()

        self._store["COM-001"] = [
            OrderSummary(
                order_id="PED-0789",
                customer="Ana Gómez",
                status=OrderStatus.RECEIVED,
                total=18500,
                products=[
                    ProductSummary("Agua 500ml", 2),
                    ProductSummary("Pan tajado", 1),
                ],
                notes="Sin sal por favor",
                created_at=now - timedelta(minutes=5),
            ),
            OrderSummary(
                order_id="PED-0790",
                customer="Carlos Ríos",
                status=OrderStatus.IN_PREPARATION,
                total=32000,
                products=[
                    ProductSummary("Jugo de naranja", 1),
                    ProductSummary("Sándwich pollo", 2),
                ],
                notes=None,
                created_at=now - timedelta(minutes=20),
            ),
            OrderSummary(
                order_id="PED-0788",
                customer="Luisa Martínez",
                status=OrderStatus.READY_FOR_PICKUP,
                total=9500,
                products=[
                    ProductSummary("Café americano", 1),
                ],
                notes="Extra caliente",
                created_at=now - timedelta(hours=1),
            ),
            OrderSummary(
                order_id="PED-0787",
                customer="Pedro Vargas",
                status=OrderStatus.DELIVERED,
                total=45000,
                products=[
                    ProductSummary("Almuerzo ejecutivo", 3),
                    ProductSummary("Agua 1.5L", 3),
                ],
                notes=None,
                created_at=now - timedelta(hours=3),
            ),
            OrderSummary(
                order_id="PED-0786",
                customer="María Suárez",
                status=OrderStatus.CANCELLED,
                total=12000,
                products=[
                    ProductSummary("Torta de chocolate", 1),
                ],
                notes="Cambié de opinión",
                created_at=now - timedelta(hours=5),
            ),
        ]

        # COM-002 is registered but has no orders (tests case 3)
        self._store["COM-002"] = []


merchant_order_repository = MerchantOrderRepository()
