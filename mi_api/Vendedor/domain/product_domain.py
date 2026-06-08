from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import uuid4

# ----- Input/output schemas -----
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: Optional[int] = Field(default=0, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name_no_numbers(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError("Name cannot contain numbers")
        return v

# ----- Internal entity (with ID and availability) -----
class Product(ProductCreate):
    product_id: str = Field(default_factory=lambda: f"P-{uuid4().hex[:6].upper()}")
    available: bool = False

    def update_availability(self):
        self.available = self.stock > 0