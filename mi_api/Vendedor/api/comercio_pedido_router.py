from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import Optional

from mi_api.Vendedor.service.comercio_pedido_service import merchant_order_service

router = APIRouter(prefix="/api/v1/merchants")


@router.patch(
    "/{merchant_id}/orders/{order_id}/status",
    tags=["Orders"],
    summary="Toggle order preparation status",
    description=(
        "Toggles the order between `received` ↔ `in_preparation` with no body required.\n\n"
        "- `received` → `in_preparation` (merchant starts preparing)\n"
        "- `in_preparation` → `received` (undo if needed)\n\n"
        "Once ready, use **Mark Ready For Pickup** to advance further."
    ),
)
def toggle_order_status_endpoint(merchant_id: str, order_id: str):
    try:
        result = merchant_order_service.toggle_order_status(merchant_id, order_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{id}/orders", tags=["Queries"], summary="List merchant orders")
def get_merchant_orders_endpoint(
    id: str,
    status_filter: Optional[str] = Query(None, alias="status"),
):
    try:
        result = merchant_order_service.get_merchant_orders(id, status_filter)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
