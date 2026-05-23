# ─────────────────────────────────────────────────────────────
# CAPA DOMINIO — Repartidor/domain/dealer_domain.py
# ─────────────────────────────────────────────────────────────
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal

# Reglas de tipos del negocio
VehicleType = Literal["moto", "bicycle", "car"]
DealerStatus = Literal["pendiente_activacion", "active", "inactive"]

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
            raise ValueError("La contraseña debe tener mínimo 8 caracteres e incluir al menos un número.")
        return v

# ── Schemas de SALIDA (Contrato JSON traducido a inglés) ──────
class DealerResponseData(BaseModel):
    driver_id: str
    name: str
    status: DealerStatus

class DealerRegisterSuccessResponse(BaseModel):
    message: str
    data: DealerResponseData
    success: bool = True

class DealerRegisterErrorResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    success: bool = False

# ── Entidad del Dominio ────────────
class Dealer:
    def __init__(self, dealer_id: str, full_name: str, phone: str, 
                 email: str, vehicle_type: VehicleType, license_number: str, 
                 status: DealerStatus = "pendiente_activacion"):
        self.dealer_id = dealer_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.vehicle_type = vehicle_type
        self.license_number = license_number
        self.status = status

    def to_dict(self) -> dict:
        return {
            "driver_id": self.dealer_id,
            "name": self.full_name,
            "status": self.status
        }