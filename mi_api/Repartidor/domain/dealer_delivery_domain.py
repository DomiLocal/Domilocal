# ─────────────────────────────────────────────────────────────
# CAPA DOMINIO (HU-C03) — Repartidor/domain/dealer_delivery_domain.py
# ─────────────────────────────────────────────────────────────
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order:
    def __init__(self, order_id: str, status: str, dealer_id: Optional[str] = None):
        self.order_id = order_id
        self.status = status          # received | in_preparation | in_transit | delivered
        self.dealer_id = dealer_id
        self.delivery_time: Optional[datetime] = None


# ── Schemas de SALIDA (HU-C03) ──────────────────────────────
class DeliveryConfirmationResponseData(BaseModel):
    order_id: str
    status: str
    delivery_time: str
    driver_status: str

class DeliveryConfirmationSuccessResponse(BaseModel):
    message: str
    data: DeliveryConfirmationResponseData
    success: bool = True

class DeliveryConfirmationErrorResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    success: bool = False
