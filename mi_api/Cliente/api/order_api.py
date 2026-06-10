from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


from domain.order_domain import (
    OrderCreate,
    OrderCancellationRequest
)

from service.order_service import OrderService
from repository.order_repository import order_repository
from service.order_status_service import OrderStatusService


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)

service = OrderService(
    repo=order_repository
)
status_service = OrderStatusService(
    repo=order_repository
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_order(order_data: OrderCreate):

    try:
        return service.create_order(order_data)

    except ValueError as e:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": str(e),
                "success": False
            }
        )


@router.patch(
    "/{order_id}/cancel",
    status_code=status.HTTP_200_OK
)
def cancel_order(
    order_id: str,
    cancellation_data: OrderCancellationRequest
):

    try:

        return service.cancel_order(
            order_id,
            cancellation_data
        )

    except LookupError as e:

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )

    except ValueError as e:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )
    

@router.get(
    "/{order_id}/status",
    status_code=status.HTTP_200_OK
)
def get_order_status(order_id: str):

    try:

        return status_service.get_order_status(order_id)

    except ValueError as e:

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )