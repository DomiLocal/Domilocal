# ─────────────────────────────────────────────────────────────
# CAPA API — Repartidor/api/dealer_api.py
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from domain.dealer_domain import DealerCreate, DealerRegisterSuccessResponse, DealerRegisterErrorResponse
from service.dealer_service import DealerService
from repository.dealer_repository import dealer_repository

router = APIRouter(
    prefix="/api/v1/repartidores",
    tags=["Dealers"]
)

# Inyección de dependencias manual del repositorio al servicio
service = DealerService(repo=dealer_repository)

@router.post(
    "/registro",
    status_code=status.HTTP_201_CREATED,
    response_model=DealerRegisterSuccessResponse,
    responses={
        400: {"model": DealerRegisterErrorResponse},
        409: {"model": DealerRegisterErrorResponse}
    }
)
def register_dealer(payload: DealerCreate):
    try:
        result_data = service.register(payload)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Registro exitoso. Tu cuenta está pendiente de activación.",
                "data": result_data.model_dump(),
                "success": True
            }
        )
    except ValueError as e:
        # Captura errores de lógica de negocio (Duplicados de la capa servicio) -> HTTP 409
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": str(e),
                "data": None,
                "success": False
            }
        )