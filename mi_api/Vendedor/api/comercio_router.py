# ─────────────────────────────────────
# CAPA API
# Endpoints HTTP
# ─────────────────────────────────────

from fastapi import (

    APIRouter,
    HTTPException,
    status

)

from domain.comercio import (

    ComercioCreate,
    RegistroComercioResponse

)

from service.comercio_service import (

    ComercioService

)

from repository.comercio_repository import (

    comercio_repository

)


router=APIRouter(

    prefix="/api/v1/comercios",

    tags=["Comercios"]

)


service=ComercioService(
    repo=comercio_repository
)


@router.post(

    "/registro",

    response_model=RegistroComercioResponse,

    status_code=status.HTTP_201_CREATED

)

def registrar_comercio(
    datos:ComercioCreate
):


    try:

        return service.registrar(
            datos
        )


    except ValueError as e:


        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,

            detail=str(e)

        )


    except Exception:


        raise HTTPException(

            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,

            detail="Base de datos no disponible"

        )
