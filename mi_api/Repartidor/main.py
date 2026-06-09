# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA GLOBAL — Repartidor/main.py
# ─────────────────────────────────────────────────────────────
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Importamos ambos controladores separados
from api.dealer_api import router as dealer_registration_router
from api.dealer_assignment_api import router as dealer_assignment_router
from api.dealer_delivery_api import router as dealer_delivery_router
from api.dealer_active_order_api import router as dealer_active_order_router

app = FastAPI(
    title="Delivery App - Central API (Multi-HU)",
    version="1.0.0"
)

# Interceptor global para transformar errores de validación de Pydantic a HTTP 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msg = "Invalid request data."
    
    if errors:
        first_error = errors[0]
        if "Value error, " in first_error["msg"]:
            error_msg = first_error["msg"].replace("Value error, ", "")
        elif first_error["type"] == "missing":
            missing_field = first_error["loc"][-1]
            error_msg = f"The field '{missing_field}' is required."
        else:
            error_msg = first_error["msg"]

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": error_msg,
            "data": None,
            "success": False
        }
    )

# Registramos de forma independiente ambos módulos en la misma app de Uvicorn
app.include_router(dealer_registration_router)
app.include_router(dealer_assignment_router)
app.include_router(dealer_delivery_router)
app.include_router(dealer_active_order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)