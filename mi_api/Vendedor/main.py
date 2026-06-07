# ─────────────────────────────────────────────────────────────
# ENTRY POINT — Vendedor/main.py (Multi-HU integration)
# Registers router for HU-C04 (Consulta de Pedidos) and other HU routers.
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Router for HU-C04: Consulta de pedidos
from api.comercio_pedido_router import router as merchant_order_router

# Let's import the existing patch router from estado_pedido if available
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from estado_pedido.api.pedido_router import router as estado_pedido_router
except ImportError:
    estado_pedido_router = None

try:
    from Gestio_productos.api.v1.product_router import router as product_router
except ImportError:
    product_router = None


app = FastAPI(
    title="Merchant Catalog & Orders API - Vendedor",
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

# Register routers
app.include_router(merchant_order_router)

if estado_pedido_router:
    app.include_router(estado_pedido_router)

if product_router:
    app.include_router(product_router)


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Vendedor API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
