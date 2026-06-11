from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# ── Cliente routers ───────────────────────────────────────────
from mi_api.Cliente.api.client_api import router as client_router
from mi_api.Cliente.api.order_api import router as order_router
from mi_api.Cliente.api.catalog_api import router as catalog_router

# ── Repartidor routers ────────────────────────────────────────
from mi_api.Repartidor.api.dealer_api import router as dealer_router
from mi_api.Repartidor.api.dealer_assignment_api import router as dealer_assignment_router
from mi_api.Repartidor.api.dealer_delivery_api import router as dealer_delivery_router
from mi_api.Repartidor.api.dealer_active_order_api import router as dealer_active_order_router

# ── Vendedor routers ──────────────────────────────────────────
from mi_api.Vendedor.api.comercio_router import router as comercio_router
from mi_api.Vendedor.api.merchant_status_router import router as merchant_status_router
from mi_api.Vendedor.api.comercio_pedido_router import router as merchant_order_router
from mi_api.Vendedor.api.pedido_router import router as pedido_router
from mi_api.Vendedor.api.v1.product_router import router as product_router

# ── Swagger tag order ─────────────────────────────────────────
openapi_tags = [
    {"name": "Registration", "description": "Register clients, merchants, and dealers"},
    {"name": "Confirmation", "description": "Activate registered accounts"},
    {"name": "Status & Availability", "description": "Toggle operational status and dealer availability"},
    {"name": "Product Management", "description": "Create, update, and delete products from merchant catalog"},
    {"name": "Orders", "description": "Full order lifecycle: create → prepare → ready → assign → deliver / cancel"},
    {"name": "Queries", "description": "Retrieve status, lists, and catalog information"},
]

# ── FastAPI app ───────────────────────────────────────────────
app = FastAPI(
    title="DomiLocal API",
    description=(
        "Plataforma de domicilios DomiLocal.\n\n"
        "Módulos integrados:\n"
        "- **Cliente**: registro, pedidos, catálogo, estado de pedido\n"
        "- **Repartidor**: registro, disponibilidad, asignación, entrega\n"
        "- **Vendedor**: registro de comercio, gestión de pedidos, catálogo de productos\n\n"
        "Todos los módulos comparten el mismo almacén de datos en memoria."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)


# ── Global exception handlers ─────────────────────────────────
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "data": None, "success": False},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_msg = "Invalid request data."

    if errors:
        first_error = errors[0]
        if "Value error, " in first_error.get("msg", ""):
            error_msg = first_error["msg"].replace("Value error, ", "")
        elif first_error.get("type") == "missing":
            missing_field = first_error.get("loc", ["unknown"])[-1]
            error_msg = f"The field '{missing_field}' is required."
        else:
            error_msg = first_error.get("msg", error_msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": error_msg, "data": None, "success": False},
    )


# ── Register routers in workflow order ────────────────────────
# Registration
app.include_router(client_router)
app.include_router(comercio_router)
app.include_router(dealer_router)

# Confirmation + Status & Availability
app.include_router(merchant_status_router)

# Product Management
app.include_router(product_router)

# Orders
app.include_router(order_router)
app.include_router(merchant_order_router)
app.include_router(pedido_router)
app.include_router(dealer_assignment_router)
app.include_router(dealer_delivery_router)

# Queries
app.include_router(catalog_router)
app.include_router(dealer_active_order_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "DomiLocal API is running",
        "docs": "/docs",
        "version": "1.0.0",
        "modules": ["Cliente", "Repartidor", "Vendedor"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
