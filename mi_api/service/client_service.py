from typing import List, Optional
from domain.models import Client, UserRole
from repository.client_repo import client_repo
from fastapi import HTTPException

class ClientService:
    def register_client(self, client: Client) -> Client:
        if client_repo.get_by_email(client.correo):
            raise HTTPException(status_code=409, detail="El correo electrónico ya se encuentra registrado.")
        
        # Simple password validation (already handled by pydantic min_length, but let's add number check)
        if not any(char.isdigit() for char in client.password):
            raise HTTPException(status_code=400, detail="La contraseña debe incluir al menos un número.")
            
        client.rol = UserRole.CLIENTE
        return client_repo.create(client)

    def get_client(self, client_id: str) -> Optional[Client]:
        return client_repo.get_by_id(client_id)

client_service = ClientService()
