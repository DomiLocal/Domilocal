# ─────────────────────────────────────
# DOMAIN LAYER
# Catalog response models
# ─────────────────────────────────────

from pydantic import BaseModel
from typing import Optional


class CatalogProductResponse(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str
    photo_url: Optional[str] = None


class CatalogDataResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    products: list[CatalogProductResponse]


class CatalogResponse(BaseModel):
    message: str
    data: Optional[CatalogDataResponse]
    success: bool