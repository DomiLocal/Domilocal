# ─────────────────────────────────────────────────────────────
# CAPA DOMINIO (HU2) — Repartidor/domain/dealer_assignment_domain.py
# ─────────────────────────────────────────────────────────────
from pydantic import BaseModel
from typing import Optional

class AssignmentResponseData(BaseModel):
    order_id: str
    dealer_id: str
    dealer_name: str
    acceptance_timeout_seconds: int = 60

class DealerAssignmentSuccessResponse(BaseModel):
    message: str
    data: AssignmentResponseData
    success: bool = True

class DealerAssignmentErrorResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    success: bool = False