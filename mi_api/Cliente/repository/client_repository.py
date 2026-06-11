from mi_api.Cliente.domain.client_domain import Client
from typing import Optional


class ClientRepository:

    def __init__(self):
        self._clients: list[Client] = []
        self._next_id: int = 1

    def _generate_client_id(self) -> str:
        client_id = f"C-{self._next_id:05d}"
        self._next_id += 1
        return client_id

    def get_all(self) -> list[Client]:
        return self._clients.copy()

    def get_by_email(self, email: str) -> Optional[Client]:
        return next(
            (c for c in self._clients if c.email.lower() == email.lower()),
            None,
        )

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def get_by_id(self, client_id: str) -> Optional[Client]:
        return next((c for c in self._clients if c.client_id == client_id), None)

    def create(
        self,
        full_name: str,
        email: str,
        password: str,
        phone: str,
        main_address: str,
        role: str = "client",
    ) -> Client:
        new_client = Client(
            client_id=self._generate_client_id(),
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            main_address=main_address,
            role=role,
        )
        self._clients.append(new_client)
        return new_client


client_repository = ClientRepository()
