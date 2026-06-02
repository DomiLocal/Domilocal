# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.client_api import router as client_router


# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal API",
    description="REST API with layered architecture using FastAPI",
    version="1.0.0"
)


# ── Global exception handler for validation errors (422 → 400) ──
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    
    # Get the first validation error
    error = exc.errors()[0]
    error_location = error.get("loc", [])
    error_type = error.get("type", "")
    error_message = error.get("msg", "Validation error")
    
    # Caso 4 — Missing required fields
    if error_type == "missing":
        field_name = error_location[-1] if error_location else "unknown"
        
        # Map field names to user-friendly messages
        field_messages = {
            "full_name": "The 'full_name' field is required.",
            "email": "The 'email' field is required.",
            "password": "The 'password' field is required.",
            "phone": "The 'phone' field is required.",
            "main_address": "The 'main_address' field is required."
        }
        
        message = field_messages.get(field_name, f"The field '{field_name}' is required.")
    
    # Case 3 — Invalid password
    elif "password" in error_location:
        message = "Password must be at least 8 characters long and include at least one number."
    
    # Case 5 — Invalid email format (if applicable)
    elif "email" in error_location and "value_error" in error_type:
        message = "The email address is not valid."
    
    # Case 1 — Invalid full name (with numbers)
    elif "full_name" in error_location:
        if "numbers" in error_message.lower():
            message = "Full name cannot contain numbers."
        else:
            message = "Full name must have at least 2 characters."
    
    # Case 6 — Invalid phone
    elif "phone" in error_location:
        if "10 digits" in error_message:
            message = "Phone number must be exactly 10 digits."
        elif "only numbers" in error_message:
            message = "Phone number must contain only numbers."
        elif "start with number 3" in error_message:
            message = "Colombian phone numbers must start with the digit 3."
        else:
            message = "Phone number is not valid."
    
    # Case 7 — Invalid address
    elif "main_address" in error_location:
        message = "Main address must have at least 5 characters."
    
    # Other validation errors
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


# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():

    return {
        "message": "DomiLocal API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }


# ── Run directly with: python main.py ───────────────────────
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
