# ─────────────────────────────────────────────────────────────
# CAPA API (HU-C03) — Repartidor/api/dealer_delivery_api.py
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from domain.dealer_delivery_domain import (
    DeliveryConfirmationSuccessResponse,
    DeliveryConfirmationErrorResponse,
)
from service.dealer_delivery_service import DealerDeliveryService
from repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter(
    prefix="/api/v1",
    tags=["Delivery Confirmation (HU-C03)"]
)


@router.patch(
    "/pedidos/{id}/confirmar-entrega",
    status_code=status.HTTP_200_OK,
    response_model=DeliveryConfirmationSuccessResponse,
    responses={
        200: {
            "model": DeliveryConfirmationSuccessResponse,
            "description": "Entrega confirmada exitosamente.",
        },
        400: {
            "model": DeliveryConfirmationErrorResponse,
            "description": "El pedido no está en estado in_transit.",
        },
        404: {
            "model": DeliveryConfirmationErrorResponse,
            "description": "Pedido no encontrado.",
        },
        503: {
            "model": DeliveryConfirmationErrorResponse,
            "description": "Base de datos no disponible.",
        },
    },
    summary="Confirm order delivery",
    description=(
        "The dealer marks an order as delivered. "
        "The order must be in `in_transit` status. "
        "Updates the status to `delivered`, records the exact delivery time "
        "and sets the dealer back to `available`."
    ),
)
def confirm_delivery(
    id: str,
    repo: DealerRepository = Depends(get_dealer_repository),
):
    service = DealerDeliveryService(repo=repo)
    try:
        result = service.confirm_delivery(id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Delivery confirmed successfully.",
                "data": result.model_dump(),
                "success": True,
            },
        )
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e), "data": None, "success": False},
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e), "data": None, "success": False},
        )
    except RuntimeError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": "Service unavailable. Please try again later.",
                "data": None,
                "success": False,
            },
        )
