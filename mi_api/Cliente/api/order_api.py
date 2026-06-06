from fastapi import APIRouter, HTTPException, status

from domain.order_domain import OrderCreate
from service.order_service import OrderService
from repository.order_repository import order_repository


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)

service = OrderService(repo=order_repository)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_order(order_data: OrderCreate):

    try:
        return service.create_order(order_data)

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )