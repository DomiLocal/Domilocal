from pydantic import BaseModel, Field, field_validator
from uuid import uuid4

VALID_CATEGORIES = {
    "restaurante",
    "farmacia",
    "tienda_de_barrio",
    "supermercado",
    "panaderia",
    "drogueria",
}

_READABLE_CATEGORIES = ", ".join(sorted(VALID_CATEGORIES))


class ComercioCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)
    category: str = Field(
        ...,
        description=(
            "Business category. Spaces or underscores both accepted. "
            f"Valid values: {_READABLE_CATEGORIES}"
        ),
    )
    phone: str = Field(..., min_length=7, max_length=15)
    email: str = Field(..., min_length=5)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        normalized = v.strip().lower().replace(" ", "_")
        if normalized not in VALID_CATEGORIES:
            raise ValueError(
                f"'{v}' is not a valid category. "
                f"Available categories: {_READABLE_CATEGORIES}"
            )
        return normalized


class Comercio:
    def __init__(self, name: str, address: str, category: str, phone: str, email: str):
        self.merchant_id = f"COM-{uuid4().hex[:3].upper()}"
        self.name = name
        self.address = address
        self.category = category
        self.phone = phone
        self.email = email
        self.status = "pending_approval"

    def to_dict(self) -> dict:
        return {
            "merchant_id": self.merchant_id,
            "name": self.name,
            "address": self.address,
            "category": self.category,
            "phone": self.phone,
            "email": self.email,
            "status": self.status,
        }
