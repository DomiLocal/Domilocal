#Define QUÉ es tu entidad (atributos) y sus reglas de negocio (validaciones, cálculos). No sabe nada de HTTP ni de base de datos.
# ─────────────────────────────────────────────────────────────
# DOMAIN LAYER — business entities and validation rules
# This layer DOES NOT import FastAPI or database logic.
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel, Field, EmailStr, field_validator
import re


# ── INPUT SCHEMA ─────────────────────────────────────────────
# Data received from the client registration form
class ClientCreate(BaseModel):

    full_name: str = Field(
        ...,
        min_length=2,
        description="Client full name"
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Password with at least 8 characters and one number"
    )

    phone: str = Field(
        ...,
        description="Colombian phone number"
    )

    main_address: str = Field(
        ...,
        min_length=5,
        description="Main address"
    )

    # ── BUSINESS RULE: full name cannot contain numbers ─────
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):

        if any(char.isdigit() for char in value):
            raise ValueError("Full name cannot contain numbers.")

        return value.strip().title()

    # ── BUSINESS RULE: email normalization ──────────────────
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):

        return value.strip().lower()

    # ── BUSINESS RULE: password validation ──────────────────
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if len(value) < 8:
            raise ValueError(
                "Password must contain at least 8 characters and one number."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least 8 characters and one number."
            )

        return value

    # ── BUSINESS RULE: Colombian phone validation ───────────
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):

        value = value.strip()

        if not value.isdigit():
            raise ValueError("Phone number must contain only numbers.")

        if len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")

        if not value.startswith("3"):
            raise ValueError(
                "Colombian phone numbers must start with number 3."
            )

        return value

    # ── BUSINESS RULE: clean address ────────────────────────
    @field_validator("main_address")
    @classmethod
    def validate_address(cls, value: str):

        return value.strip()


# ── OUTPUT SCHEMA ────────────────────────────────────────────
# Data returned to the client after registration
class ClientResponse(BaseModel):

    client_id: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


# ── INTERNAL DOMAIN ENTITY ───────────────────────────────────
# Real business entity used internally by the system
class Client:

    def __init__(
        self,
        client_id: str,
        full_name: str,
        email: str,
        password: str,
        phone: str,
        main_address: str,
        role: str = "client"
    ):

        self.client_id = client_id
        self.full_name = full_name
        self.email = email
        self.password = password
        self.phone = phone
        self.main_address = main_address
        self.role = role

    # Convert internal entity into API response format
    def to_response(self) -> dict:

        return {
            "client_id": self.client_id,
            "full_name": self.full_name,
            "role": self.role
        }
