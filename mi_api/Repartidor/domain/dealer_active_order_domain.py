# ─────────────────────────────────────────────────────────────
# DOMINIO (HU-C05) — Consulta del pedido activo del repartidor
# ─────────────────────────────────────────────────────────────
from typing import Optional
from pydantic import BaseModel


class Merchant(BaseModel):
    name: str
    address: str


class Customer(BaseModel):
    name: str
    phone: str
    delivery_address: str
    map_link: str
    notes: Optional[str] = None


class Product(BaseModel):
    name: str
    quantity: int


class ActiveOrderDetail:
    """Entidad interna con el detalle completo de un pedido activo."""
    def __init__(
        self,
        order_id: str,
        merchant: Merchant,
        customer: Customer,
        products: list[Product],
    ):
        self.order_id = order_id
        self.merchant = merchant
        self.customer = customer
        self.products = products


class ActiveOrderResponseData(BaseModel):
    order_id: str
    merchant: Merchant
    customer: Customer
    products: list[Product]


class ActiveOrderSuccessResponse(BaseModel):
    message: str
    data: ActiveOrderResponseData
    success: bool


class ActiveOrderErrorResponse(BaseModel):
    message: str
    data: None
    success: bool
