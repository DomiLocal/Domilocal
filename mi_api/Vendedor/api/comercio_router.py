# ─────────────────────────────────────
# API LAYER
# HTTP Endpoints
# ─────────────────────────────────────

from fastapi import (
    APIRouter,
    HTTPException,
    status
)

from domain.comercio import (
    MerchantCreate,
    MerchantRegistrationResponse
)

from service.comercio_service import (
    MerchantService
)

from repository.comercio_repository import (
    merchant_repository
)


router = APIRouter(
    prefix="/api/v1/merchants",
    tags=["Merchants"]
)


service = MerchantService(
    repo=merchant_repository
)


@router.post(
    "/register",
    response_model=MerchantRegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_merchant(
    data: MerchantCreate
):
    try:
        return service.register(
            data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable"
        )
