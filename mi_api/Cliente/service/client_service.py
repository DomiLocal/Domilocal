#Coordina el flujo: valida las reglas del dominio, llama al repositorio, prepara la respuesta. No accede a datos directamente.
# ─────────────────────────────────────────────────────────────
# SERVICE LAYER — business logic orchestration
# Handles workflows and business rules.
# No FastAPI or HTTP logic here.
# ─────────────────────────────────────────────────────────────

from domain.client_domain import (
    ClientCreate,
    ClientResponse
)

from repository.client_repository import ClientRepository


class ClientService:

    def __init__(self, repo: ClientRepository):

        # Dependency injection
        self.repo = repo

    # ── Register new client ──────────────────────────────────
    def register(self, data: ClientCreate) -> dict:

        # Business rule: email must be unique
        if self.repo.email_exists(data.email):

            raise ValueError(
                "Email is already registered."
            )

        # Create client
        client = self.repo.create(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            phone=data.phone,
            main_address=data.main_address,
            role="client"
        )

        # Build response
        response_data = ClientResponse(
            client_id=client.client_id,
            full_name=client.full_name,
            role=client.role
        )

        return {
            "message": "Registration successful. Welcome to DomiLocal.",
            "data": response_data.model_dump(),
            "success": True
        }

    # ── Optional helper for future testing/debugging ─────────
    def list_clients(self):

        return self.repo.get_all()
