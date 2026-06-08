# ─────────────────────────────────────
# DOMAIN LAYER
# Rules and models
# ─────────────────────────────────────

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


VALID_CATEGORIES = [
    "restaurant",
    "pharmacy",
    "corner store",
    "supermarket",
    "bakery",
    "coffee shop"
]


class MerchantCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3
    )

    address: str = Field(
        ...,
        min_length=5
    )

    category: str

    phone: str = Field(
        ...,
        min_length=10
    )

    contact_email: EmailStr

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if value.lower() not in VALID_CATEGORIES:
            raise ValueError(
                "The selected category is not valid."
            )
        return value.lower()


class MerchantResponse(BaseModel):
    id_merchant: str
    name: str
    status: str


class MerchantRegistrationResponse(BaseModel):
    message: str
    data: MerchantResponse | None
    success: bool


class Merchant:
    def __init__(
        self,
        id_merchant,
        name,
        address,
        category,
        phone,
        contact_email,
        status="pending_approval"
    ):
        self.id_merchant = id_merchant
        self.name = name
        self.address = address
        self.category = category
        self.phone = phone
        self.contact_email = contact_email
        self.status = status

    def visible_to_customers(self):
        return self.status == "active"

    def to_response(self):
        return {
            "id_merchant": self.id_merchant,
            "name": self.name,
            "status": self.status
        }
