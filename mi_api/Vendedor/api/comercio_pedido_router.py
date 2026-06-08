# ─────────────────────────────────────────────────────────────
# API ROUTER — consulta_pedidos
# Defines GET /api/v1/comercios/{id}/pedidos endpoint
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import Optional

from service.comercio_pedido_service import merchant_order_service

router = APIRouter(
    prefix="/api/v1/merchants",
    tags=["Merchant Orders"]
)


@router.get("/{id}/orders")
def get_merchant_orders_endpoint(
    id: str,
    status_filter: Optional[str] = Query(None, alias="status")
):
    try:
        result = merchant_order_service.get_merchant_orders(id, status_filter)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Technical Note: 503 if database/repository fails (simulation)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service not available."
        )
