#Guarda y recupera datos. Hoy usaremos una lista en memoria; mañana puede ser PostgreSQL — sin tocar el resto del código.
# ─────────────────────────────────────────────────────────────
# REPOSITORY LAYER — data access
# Handles storage and retrieval of client data.
# No business logic or FastAPI here.
# ─────────────────────────────────────────────────────────────

from domain.client_domain import Client
from typing import Optional


class ClientRepository:

    def __init__(self):

        # In-memory storage
        self._clients: list[Client] = []

        # Auto incremental counter
        self._next_id: int = 1

    # ── Generate formatted client ID ─────────────────────────
    def _generate_client_id(self) -> str:

        client_id = f"C-{self._next_id:05d}"
        self._next_id += 1

        return client_id

    # ── Get all clients ──────────────────────────────────────
    def get_all(self) -> list[Client]:

        return self._clients.copy()

    # ── Find client by email ─────────────────────────────────
    def get_by_email(self, email: str) -> Optional[Client]:

        return next(
            (
                client
                for client in self._clients
                if client.email.lower() == email.lower()
            ),
            None
        )

    # ── Check if email already exists ────────────────────────
    def email_exists(self, email: str) -> bool:

        return self.get_by_email(email) is not None

    # ── Create new client ────────────────────────────────────
    def create(
        self,
        full_name: str,
        email: str,
        password: str,
        phone: str,
        main_address: str,
        role: str = "client"
    ) -> Client:

        new_client = Client(
            client_id=self._generate_client_id(),
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            main_address=main_address,
            role=role
        )

        self._clients.append(new_client)

        return new_client


# Shared singleton instance
client_repository = ClientRepository()
