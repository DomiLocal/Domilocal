from pydantic import BaseModel, Field, field_validator
from typing import List


class OrderItemCreate(BaseModel):
    product_name: str = Field(..., min_length=2)
    store_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    delivery_address: str | None = None
    payment_method: str

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):
        allowed_methods = ["cash", "online_payment"]

        if value not in allowed_methods:
            raise ValueError(
                "Payment method must be 'cash' or 'online_payment'"
            )

        return value


class OrderResponse(BaseModel):
    order_id: str
    status: str
    total: float
    payment_method: str
    delivery_address: str


class Order:

    def __init__(
        self,
        order_id: str,
        items: list,
        delivery_address: str,
        payment_method: str,
        total: float,
        status: str = "received"
    ):
        self.order_id = order_id
        self.items = items
        self.delivery_address = delivery_address
        self.payment_method = payment_method
        self.total = total
        self.status = status

    def to_response(self):
        return {
            "order_id": self.order_id,
            "status": self.status,
            "total": self.total,
            "payment_method": self.payment_method,
            "delivery_address": self.delivery_address
        }


class OrderCancellationRequest(BaseModel):
    reason: str | None = None