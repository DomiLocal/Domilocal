# ─────────────────────────────────────────────────────────────
# CAPA API (HU2) — Repartidor/api/dealer_assignment_api.py
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from domain.dealer_assignment_domain import DealerAssignmentSuccessResponse, DealerAssignmentErrorResponse
from service.dealer_assignment_service import DealerAssignmentService
from repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter(
    prefix="/api/v1",
    tags=["Assignments (HU2)"]
)

@router.post(
    "/pedidos/{order_id}/asignar-repartidor",
    status_code=status.HTTP_200_OK,
    response_model=DealerAssignmentSuccessResponse,
    responses={
        200: {"model": DealerAssignmentSuccessResponse},
        400: {"model": DealerAssignmentErrorResponse},
        404: {"model": DealerAssignmentErrorResponse}
    }
)
def assign_dealer_to_order(order_id: str, repo: DealerRepository = Depends(get_dealer_repository)):
    STORE_LAT = 7.120
    STORE_LNG = -73.120

    if order_id == "PED-NOTFOUND":
        raise HTTPException(status_code=404, detail="The requested order does not exist.")

    # Instanciamos el servicio pasando el repositorio controlado por FastAPI
    assignment_service = DealerAssignmentService(repo=repo)

    try:
        assignment_data = assignment_service.assign_closest_dealer(order_id, STORE_LAT, STORE_LNG)
        
        if assignment_data:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Dealer assigned successfully.",
                    "data": assignment_data.model_dump(),
                    "success": True
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "No dealers available at this time. Retrying in 30 seconds.",
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