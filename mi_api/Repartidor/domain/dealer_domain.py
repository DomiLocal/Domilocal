# ─────────────────────────────────────────────────────────────
# CAPA DOMINIO — Repartidor/domain/dealer_domain.py
# ─────────────────────────────────────────────────────────────
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal

VehicleType = Literal["moto", "bicycle", "car"]
AccountStatus = Literal["pending_activation", "active", "inactive"]
AvailabilityStatus = Literal["available", "unavailable"]

# ── Schema de ENTRADA (Validación del formulario) ──────
class DealerCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=7)
    email: EmailStr
    password: str
    vehicle_type: VehicleType
    license_number: str = Field(..., min_length=1)

    # REGLA DE NEGOCIO: Requisitos estrictos de la contraseña (Caso 4)
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8 or not any(char.isdigit() for char in v):
            raise ValueError("Password must be at least 8 characters long and include at least one number.")
        return v

# ── Schemas de SALIDA (HU1) ──────
class DealerResponseData(BaseModel):
    dealer_id: str
    name: str
    status: AccountStatus

class DealerRegisterSuccessResponse(BaseModel):
    message: str
    data: DealerResponseData
    success: bool = True

class DealerRegisterErrorResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    success: bool = False

# ── Schemas de disponibilidad (HU3) ────────────────────────
class DealerAvailabilityResponseData(BaseModel):
    dealer_id: str
    status: AvailabilityStatus

class DealerAvailabilitySuccessResponse(BaseModel):
    message: str
    data: DealerAvailabilityResponseData
    success: bool = True

class DealerAvailabilityErrorResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    success: bool = False

# ── Entidad del Dominio ────────────
class Dealer:
    def __init__(self, dealer_id: str, full_name: str, phone: str,
                 email: str, vehicle_type: VehicleType, license_number: str,
                 account_status: AccountStatus = "pending_activation",
                 availability: Optional[AvailabilityStatus] = None):
        self.dealer_id = dealer_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.vehicle_type = vehicle_type
        self.license_number = license_number
        self.account_status = account_status
        self.availability = availability

    def to_dict(self) -> dict:
        return {
            "dealer_id": self.dealer_id,
            "name": self.full_name,
            "status": self.account_status
        }
