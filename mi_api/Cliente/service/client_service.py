from mi_api.Cliente.domain.client_domain import ClientCreate, ClientResponse
from mi_api.Cliente.repository.client_repository import ClientRepository


class ClientService:

    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def register(self, data: ClientCreate) -> dict:
        if self.repo.email_exists(data.email):
            raise ValueError("Email is already registered.")

        client = self.repo.create(
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            phone=data.phone,
            main_address=data.main_address,
            role="client",
        )

        response_data = ClientResponse(
            client_id=client.client_id,
            full_name=client.full_name,
            role=client.role,
        )

        return {
            "message": "Registration successful. Welcome to DomiLocal.",
            "data": response_data.model_dump(),
            "success": True,
        }

    def list_clients(self):
        return self.repo.get_all()
