# ─────────────────────────────────────────────────────────────
# DOMAIN — consulta_pedidos
# Entities, value objects and business rules for the
# "get orders by merchant" feature.
# ─────────────────────────────────────────────────────────────

from enum import Enum
from typing import List, Optional
from datetime import datetime


class OrderStatus(str, Enum):
    RECEIVED         = "received"
    IN_PREPARATION   = "in_preparation"
    READY_FOR_PICKUP = "ready_for_pickup"
    IN_TRANSIT       = "in_transit"
    DELIVERED        = "delivered"
    CANCELLED        = "cancelled"


class ProductSummary:
    """Lightweight product representation inside an order."""

    def __init__(self, name: str, quantity: int):
        self.name     = name
        self.quantity = quantity

    def to_dict(self) -> dict:
        return {
            "name":     self.name,
            "quantity": self.quantity,
        }


class OrderSummary:
    """
    Represents a single order belonging to a merchant.
    Encapsulates all data visible to the seller.
    """

    def __init__(
        self,
        order_id:    str,
        customer:    str,
        status:      OrderStatus,
        total:       float,
        products:    List[ProductSummary],
        notes:       Optional[str]    = None,
        created_at:  Optional[datetime] = None,
    ):
        self.order_id   = order_id
        self.customer   = customer
        self.status     = status
        self.total      = total
        self.products   = products
        self.notes      = notes
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "customer": self.customer,
            "status":   self.status.value,
            "total":    self.total,
            "products": [p.to_dict() for p in self.products],
            "notes":    self.notes,
        }
