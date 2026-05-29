# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA — main.py
# ─────────────────────────────────────────────────────────────
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.dealer_api import router as dealer_router

app = FastAPI(
    title="Delivery App - Central API",
    version="1.0.0"
)

# Interceptor global de errores de validación (Para cumplir Caso 3 y Caso 4 con HTTP 400)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msg = "Invalid request data."
    
    if errors:
        first_error = errors[0]
        # Limpieza de mensajes personalizados de Pydantic
        if "Value error, " in first_error["msg"]:
            error_msg = first_error["msg"].replace("Value error, ", "")
        # Manejo de campos faltantes obligatorios
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

# Registrar el módulo modular del Repartidor
app.include_router(dealer_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)