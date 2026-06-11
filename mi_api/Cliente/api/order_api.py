from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from mi_api.Cliente.domain.order_domain import OrderCreate, OrderCancellationRequest
from mi_api.Cliente.service.order_service import OrderService
from mi_api.Cliente.repository.order_repository import order_repository
from mi_api.Cliente.service.order_status_service import OrderStatusService

router = APIRouter(prefix="/api/v1/orders")

service = OrderService(repo=order_repository)
status_service = OrderStatusService(repo=order_repository)


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Orders"], summary="Create order")
def create_order(order_data: OrderCreate):
    try:
        return service.create_order(order_data)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e), "success": False},
        )


@router.patch("/{order_id}/cancel", status_code=status.HTTP_200_OK, tags=["Orders"], summary="Cancel order")
def cancel_order(order_id: str, cancellation_data: OrderCancellationRequest):
    try:
        return service.cancel_order(order_id, cancellation_data)
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


@router.get("/{order_id}/status", status_code=status.HTTP_200_OK, tags=["Queries"], summary="Get order status")
def get_order_status(order_id: str):
    try:
        return status_service.get_order_status(order_id)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e), "data": None, "success": False},
        )
