from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from domain.comercio_domain import ComercioCreate
from service.comercio_service import comercio_service

router = APIRouter(
    prefix="/api/v1/comercios",
    tags=["Registro de Comercio"]
)


@router.post("/registro", status_code=status.HTTP_201_CREATED)
def register_comercio(data: ComercioCreate):
    try:
        result = comercio_service.register_comercio(data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": str(e),
                "data": None,
                "success": False,
            },
        )
