import asyncio
from fastapi import APIRouter, status, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse

from mi_api.Repartidor.domain.dealer_assignment_domain import (
    DealerAssignmentSuccessResponse, DealerAssignmentErrorResponse,
)
from mi_api.Repartidor.service.dealer_assignment_service import DealerAssignmentService
from mi_api.Repartidor.repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter(prefix="/api/v1", tags=["Orders"])

STORE_LAT = 7.120
STORE_LNG = -73.120


async def _schedule_timeout_reassignment(order_id: str, dealer_id: str, repo: DealerRepository):
    await asyncio.sleep(60)
    service = DealerAssignmentService(repo=repo)
    result = service.reassign_after_timeout(order_id, dealer_id, STORE_LAT, STORE_LNG)
    if result:
        print(f"[REASSIGNMENT] Order {order_id} reassigned to dealer {result.dealer_id} after 60s timeout")
    else:
        print(f"[REASSIGNMENT] Order {order_id}: no action (accepted or no dealers available)")


@router.post(
    "/orders/{order_id}/assign-dealer",
    status_code=status.HTTP_200_OK,
    response_model=DealerAssignmentSuccessResponse,
    responses={
        200: {"model": DealerAssignmentSuccessResponse},
        400: {"model": DealerAssignmentErrorResponse},
        404: {"model": DealerAssignmentErrorResponse},
    },
)
async def assign_dealer_to_order(
    order_id: str,
    background_tasks: BackgroundTasks,
    simular_timeout: bool = Query(default=False, description="Simulate that the assigned dealer does not accept within 60 seconds"),
    repo: DealerRepository = Depends(get_dealer_repository),
):
    from mi_api.shared_store import ORDERS
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="The requested order does not exist.")

    service = DealerAssignmentService(repo=repo)

    try:
        assignment_data = service.assign_closest_dealer(order_id, STORE_LAT, STORE_LNG)

        if not assignment_data:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "No drivers available at this time. Retrying in 30 seconds.",
                    "data": None,
                    "success": False,
                },
            )

        if simular_timeout:
            result = service.reassign_after_timeout(order_id, assignment_data.dealer_id, STORE_LAT, STORE_LNG)
            if result:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": f"Dealer {assignment_data.dealer_id} did not accept. Reassigned to dealer {result.dealer_id}.",
                        "data": result.model_dump(),
                        "success": True,
                    },
                )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": f"Dealer {assignment_data.dealer_id} did not accept. No other dealers available.",
                    "data": None,
                    "success": False,
                },
            )

        background_tasks.add_task(_schedule_timeout_reassignment, order_id, assignment_data.dealer_id, repo)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Driver assigned successfully.", "data": assignment_data.model_dump(), "success": True},
        )

    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e), "data": None, "success": False},
        )
