# ─────────────────────────────────────────────────────────────
# CAPA API (HU1) — Repartidor/api/dealer_api.py
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from domain.dealer_domain import DealerCreate, DealerRegisterSuccessResponse, DealerRegisterErrorResponse
from service.dealer_service import DealerService
from repository.dealer_repository import DealerRepository, get_dealer_repository

router = APIRouter(
    prefix="/api/v1/repartidores",
    tags=["Dealers"]
)

@router.post(
    "/registro",
    status_code=status.HTTP_201_CREATED,
    response_model=DealerRegisterSuccessResponse,
    responses={
        400: {"model": DealerRegisterErrorResponse},
        409: {"model": DealerRegisterErrorResponse}
    }
)
def register_dealer(payload: DealerCreate, repo: DealerRepository = Depends(get_dealer_repository)):
    # Se genera el servicio con el repositorio unificado de FastAPI
    registration_service = DealerService(repo=repo)
    try:
        result_data = registration_service.register(payload)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Registration successful. Your account is pending activation.",
                "data": result_data.model_dump(),
                "success": True
            }
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )