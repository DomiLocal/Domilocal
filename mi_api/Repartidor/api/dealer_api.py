# ─────────────────────────────────────────────────────────────
# CAPA API (HU1) — Repartidor/api/dealer_api.py
# ─────────────────────────────────────────────────────────────
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from domain.dealer_domain import (
    DealerCreate, DealerRegisterSuccessResponse, DealerRegisterErrorResponse,
    DealerAvailabilitySuccessResponse, DealerAvailabilityErrorResponse
)
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


@router.post(
    "/{dealer_id}/confirmar",
    status_code=status.HTTP_200_OK,
    response_model=DealerRegisterSuccessResponse,
    responses={
        404: {"model": DealerRegisterErrorResponse},
        409: {"model": DealerRegisterErrorResponse}
    }
)
def confirm_dealer(dealer_id: str, repo: DealerRepository = Depends(get_dealer_repository)):
    service = DealerService(repo=repo)
    try:
        result = service.confirm_dealer(dealer_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Account confirmed successfully.",
                "data": result.model_dump(),
                "success": True
            }
        )
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e), "data": None, "success": False}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(e), "data": None, "success": False}
        )


@router.patch(
    "/{dealer_id}/disponibilidad",
    status_code=status.HTTP_200_OK,
    response_model=DealerAvailabilitySuccessResponse,
    responses={
        400: {"model": DealerAvailabilityErrorResponse},
        404: {"model": DealerAvailabilityErrorResponse}
    }
)
def toggle_availability(dealer_id: str, repo: DealerRepository = Depends(get_dealer_repository)):
    service = DealerService(repo=repo)
    try:
        result = service.toggle_availability(dealer_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Availability status updated successfully.",
                "data": result.model_dump(),
                "success": True
            }
        )
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e), "data": None, "success": False}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e), "data": None, "success": False}
        )
