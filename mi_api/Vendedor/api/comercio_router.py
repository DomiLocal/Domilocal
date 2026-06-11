from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from mi_api.Vendedor.domain.comercio_domain import ComercioCreate
from mi_api.Vendedor.service.comercio_service import comercio_service

router = APIRouter(prefix="/api/v1/merchants", tags=["Registration"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register Merchant",
    description=(
        "Register a new merchant on the platform.\n\n"
        "**Available categories** (spaces or underscores both accepted):\n"
        "- `restaurante`\n"
        "- `farmacia`\n"
        "- `tienda_de_barrio` / `tienda de barrio`\n"
        "- `supermercado`\n"
        "- `panaderia`\n"
        "- `drogueria`\n\n"
        "New merchants start with status `pending_approval`. "
        "Use `POST /merchants/{id}/confirm` to activate."
    ),
)
def register_comercio(data: ComercioCreate):
    try:
        result = comercio_service.register_comercio(data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(e), "data": None, "success": False},
        )
