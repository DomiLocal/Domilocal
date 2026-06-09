# ─────────────────────────────────────────────────────────────
# API (HU-C05) — Consulta del pedido activo del repartidor
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from domain.dealer_active_order_domain import (
    ActiveOrderResponseData,
    ActiveOrderSuccessResponse,
    ActiveOrderErrorResponse,
)
from service.dealer_active_order_service import DealerActiveOrderService
from repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter()


@router.get(
    "/api/v1/repartidores/{id}/pedido-activo",
    summary="Get active order details",
    description=(
        "Returns the full details of the active order assigned to the dealer: "
        "merchant info, customer data, delivery address with map link, "
        "product list, and special notes."
    ),
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": ActiveOrderSuccessResponse},
        404: {"model": ActiveOrderErrorResponse},
        503: {"model": ActiveOrderErrorResponse},
    },
    tags=["HU-C05 — Active Order Query"],
)
def get_active_order(
    id: str,
    repo: DealerRepository = Depends(get_dealer_repository),
):
    service = DealerActiveOrderService(repo)
    try:
        detail, reason = service.get_active_order(id)
    except RuntimeError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "Service unavailable. Please try again later.", "data": None, "success": False},
        )

    if reason == "dealer_not_found":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Dealer not found.", "data": None, "success": False},
        )

    if reason == "no_active_order":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "You have no active order at this moment.", "data": None, "success": False},
        )

    response_data = ActiveOrderResponseData(
        order_id=detail.order_id,
        merchant=detail.merchant,
        customer=detail.customer,
        products=detail.products,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Order details retrieved successfully.",
            "data": response_data.model_dump(),
            "success": True,
        },
    )
