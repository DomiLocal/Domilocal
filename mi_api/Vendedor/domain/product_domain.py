from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import uuid4

VALID_PRODUCT_CATEGORIES = {
    "bebidas", "comidas", "panaderia", "lacteos",
    "snacks", "aseo", "mascotas", "general",
}

_READABLE_PRODUCT_CATEGORIES = ", ".join(sorted(VALID_PRODUCT_CATEGORIES))


# ----- Input/output schemas -----
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: Optional[int] = Field(default=0, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    category: str = Field(
        default="general",
        description=f"Product category. Valid values: {_READABLE_PRODUCT_CATEGORIES}",
    )

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        normalized = v.strip().lower().replace(" ", "_")
        if normalized not in VALID_PRODUCT_CATEGORIES:
            raise ValueError(
                f"'{v}' is not a valid product category. "
                f"Available categories: {_READABLE_PRODUCT_CATEGORIES}"
            )
        return normalized


# ----- Internal entity (with ID and availability) -----
class Product(ProductCreate):
    product_id: str = Field(default_factory=lambda: f"P-{uuid4().hex[:6].upper()}")
    available: bool = False

    def update_availability(self):
        self.available = self.stock > 0