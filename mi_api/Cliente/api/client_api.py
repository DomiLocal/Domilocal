from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from mi_api.Cliente.domain.client_domain import ClientCreate
from mi_api.Cliente.service.client_service import ClientService
from mi_api.Cliente.repository.client_repository import client_repository

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Registration"]
)

service = ClientService(repo=client_repository)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_client(data: ClientCreate):
    try:
        return service.register(data)
    except ValueError as error:
        error_message = str(error)
        if error_message == "Email is already registered.":
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "Email is already registered", "data": None, "success": False},
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable.",
        )
