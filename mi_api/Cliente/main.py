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
            "full_name": "El campo 'full_name' es obligatorio.",
            "email": "El campo 'email' es obligatorio.",
            "password": "El campo 'password' es obligatorio.",
            "phone": "El campo 'phone' es obligatorio.",
            "main_address": "El campo 'main_address' es obligatorio."
        }
        
        message = field_messages.get(field_name, f"El campo '{field_name}' es obligatorio.")
    
    # Caso 3 — Invalid password
    elif "password" in error_location:
        message = "La contraseña debe tener mínimo 8 caracteres e incluir al menos un número."
    
    # Caso 5 — Invalid email format (si aplica)
    elif "email" in error_location and "value_error" in error_type:
        message = "El correo electrónico no es válido."
    
    # Caso 1 — Invalid full name (con números)
    elif "full_name" in error_location:
        if "numbers" in error_message.lower():
            message = "El nombre completo no puede contener números."
        else:
            message = "El nombre completo debe tener mínimo 2 caracteres."
    
    # Caso 6 — Invalid phone
    elif "phone" in error_location:
        if "10 digits" in error_message:
            message = "El número de teléfono debe tener exactamente 10 dígitos."
        elif "only numbers" in error_message:
            message = "El número de teléfono debe contener solo números."
        elif "start with number 3" in error_message:
            message = "Los números de teléfono colombianos deben empezar con el número 3."
        else:
            message = "El número de teléfono no es válido."
    
    # Caso 7 — Invalid address
    elif "main_address" in error_location:
        message = "La dirección principal debe tener mínimo 5 caracteres."
    
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