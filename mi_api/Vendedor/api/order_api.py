from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from service.order_service import OrderService
from repository.order_repository import order_repository, DatabaseConnectionError

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Vendedor Orders"]
)

service = OrderService(repo=order_repository)


@router.patch(
    "/{order_id}/ready-for-pickup",
    status_code=status.HTTP_200_OK
)
def mark_as_ready_for_pickup(order_id: str):
    try:
        result = service.mark_order_as_ready(order_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    except ValueError as e:
        # Invalid status transition (HTTP 400)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )

    except KeyError as e:
        # Order not found (HTTP 404)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": str(e).strip("'"),
                "data": None,
                "success": False
            }
        )

    except DatabaseConnectionError as e:
        # Database not available (HTTP 503)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )

    except Exception as e:
        # General server error (HTTP 500)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": f"Internal server error: {str(e)}",
                "data": None,
                "success": False
            }
        )
