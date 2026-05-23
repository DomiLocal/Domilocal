#Recibe las peticiones HTTP, llama al servicio, devuelve la respuesta. No contiene lógica de negocio.

# ─────────────────────────────────────────────────────────────
# API LAYER — HTTP routes with FastAPI
# Receives requests and calls the service layer.
# No business logic here.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, status

from domain.client_domain import ClientCreate

from service.client_service import ClientService

from repository.client_repository import client_repository


# ── Router configuration ─────────────────────────────────────
router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"]
)

# ── Service instance with dependency injection ──────────────
service = ClientService(repo=client_repository)


# ── POST /api/v1/clients/register ───────────────────────────
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register_client(data: ClientCreate):

    try:

        return service.register(data)

    except ValueError as error:

        error_message = str(error)

        # Duplicate email
        if error_message == "Email is already registered.":

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_message
            )

        # Validation/business errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )

    # Future database errors
    except Exception:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable."
        )