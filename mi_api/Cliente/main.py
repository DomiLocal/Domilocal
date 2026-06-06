# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.client_api import router as client_router
from api.order_api import router as order_router


# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal API",
    description="REST API with layered architecture using FastAPI",
    version="1.0.0"
)


# ── Global exception handler for validation errors (422 → 400) ──
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    error = exc.errors()[0]
    error_location = error.get("loc", [])
    error_type = error.get("type", "")
    error_message = error.get("msg", "Validation error")

    # Missing required fields
    if error_type == "missing":
        field_name = error_location[-1] if error_location else "unknown"

        field_messages = {
            "full_name": "The 'full_name' field is required.",
            "email": "The 'email' field is required.",
            "password": "The 'password' field is required.",
            "phone": "The 'phone' field is required.",
            "main_address": "The 'main_address' field is required.",

            # Order fields
            "merchant_id": "The 'merchant_id' field is required.",
            "items": "The 'items' field is required.",
            "delivery_address": "The 'delivery_address' field is required.",
            "payment_method": "The 'payment_method' field is required."
        }

        message = field_messages.get(
            field_name,
            f"The field '{field_name}' is required."
        )

    # Client validations
    elif "password" in error_location:
        message = "Password must be at least 8 characters long and include at least one number."

    elif "email" in error_location:
        message = "The email address is not valid."

    elif "full_name" in error_location:
        message = "Full name is not valid."

    elif "phone" in error_location:
        message = "Phone number is not valid."

    elif "main_address" in error_location:
        message = "Main address is not valid."

    # Order validations
    elif "delivery_address" in error_location:
        message = "Delivery address is required."

    elif "payment_method" in error_location:
        message = "Payment method is required."

    else:
        message = error_message

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": message,
            "data": None,
            "success": False
        }
    )


# ── Register routers ─────────────────────────────────────────
app.include_router(client_router)
app.include_router(order_router)


# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():

    return {
        "message": "DomiLocal API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }


# ── Run directly with: python main.py ────────────────────────
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )