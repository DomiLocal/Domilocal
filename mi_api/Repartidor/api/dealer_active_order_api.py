from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from mi_api.Repartidor.domain.dealer_active_order_domain import (
    ActiveOrderResponseData,
    ActiveOrderSuccessResponse,
    ActiveOrderErrorResponse,
)
from mi_api.Repartidor.service.dealer_active_order_service import DealerActiveOrderService
from mi_api.Repartidor.repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter()


@router.get(
    "/api/v1/dealers/{id}/active-order",
    summary="Get active order details",
    description=(
        "Returns full details of the active order assigned to the dealer: "
        "merchant info, customer data, delivery address with map link, "
        "product list, and special notes."
    ),
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ActiveOrderSuccessResponse},
        404: {"model": ActiveOrderErrorResponse},
        503: {"model": ActiveOrderErrorResponse},
    },
    tags=["Queries"],
)
def get_active_order(id: str, repo: DealerRepository = Depends(get_dealer_repository)):
    service = DealerActiveOrderService(repo)
    try:
        detail, reason = service.get_active_order(id)
    except RuntimeError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "Service unavailable. Please try again later.", "data": None, "success": False},
        )

    if reason == "dealer_not_found":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Dealer not found.", "data": None, "success": False})

    if reason == "no_active_order":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "You have no active order at this moment.", "data": None, "success": False})

    response_data = ActiveOrderResponseData(
        order_id=detail.order_id,
        merchant=detail.merchant,
        customer=detail.customer,
        products=detail.products,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Order details retrieved successfully.", "data": response_data.model_dump(), "success": True},
    )
