from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from mi_api.Repartidor.domain.dealer_delivery_domain import (
    DeliveryConfirmationSuccessResponse,
    DeliveryConfirmationErrorResponse,
)
from mi_api.Repartidor.service.dealer_delivery_service import DealerDeliveryService
from mi_api.Repartidor.repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter(prefix="/api/v1", tags=["Orders"])


@router.patch(
    "/orders/{id}/confirm-delivery",
    status_code=status.HTTP_200_OK,
    response_model=DeliveryConfirmationSuccessResponse,
    responses={
        200: {"model": DeliveryConfirmationSuccessResponse, "description": "Delivery confirmed."},
        400: {"model": DeliveryConfirmationErrorResponse, "description": "Order not in_transit."},
        404: {"model": DeliveryConfirmationErrorResponse, "description": "Order not found."},
        503: {"model": DeliveryConfirmationErrorResponse, "description": "Database unavailable."},
    },
    summary="Confirm order delivery",
    description=(
        "The dealer marks an order as delivered. "
        "Order must be in `in_transit` status. "
        "Updates status to `delivered`, records delivery time, and sets dealer to `available`."
    ),
)
def confirm_delivery(id: str, repo: DealerRepository = Depends(get_dealer_repository)):
    service = DealerDeliveryService(repo=repo)
    try:
        result = service.confirm_delivery(id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Delivery confirmed successfully.", "data": result.model_dump(), "success": True},
        )
    except LookupError as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e), "data": None, "success": False})
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e), "data": None, "success": False})
    except RuntimeError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "Service unavailable. Please try again later.", "data": None, "success": False},
        )
