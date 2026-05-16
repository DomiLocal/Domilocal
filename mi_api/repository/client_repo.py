from typing import List, Optional
from domain.models import Client

class ClientRepository:
    def __init__(self):
        self._clients: List[Client] = []
        self._counter = 1

    def create(self, client: Client) -> Client:
        client.id_cliente = f"C-{self._counter:05d}"
        self._clients.append(client)
        self._counter += 1
        return client

    def get_by_email(self, email: str) -> Optional[Client]:
        return next((c for c in self._clients if c.correo == email), None)

    def get_by_id(self, client_id: str) -> Optional[Client]:
        return next((c for c in self._clients if c.id_cliente == client_id), None)

client_repo = ClientRepository()
