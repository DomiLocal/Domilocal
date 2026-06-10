import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.comercio_router import router as comercio_router
from api.comercio_pedido_router import router as merchant_order_router
from api.pedido_router import router as pedido_router
from api.v1.product_router import router as product_router


app = FastAPI(
    title="Vendedor API — DomiLocal",
    version="1.0.0"
)


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
        content={"message": error_msg, "data": None, "success": False},
    )


# comercio_router must be registered before merchant_order_router so that the
# static path /registro is matched before the dynamic /{id}/pedidos segment.
app.include_router(comercio_router)
app.include_router(merchant_order_router)
app.include_router(pedido_router)
app.include_router(product_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Vendedor API is running successfully",
        "docs": "/docs",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
