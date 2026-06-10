from typing import Dict, Any
from domain.comercio_domain import ComercioCreate, Comercio
from repository.comercio_repository import ComercioRepository, comercio_repository


class ComercioService:

    def __init__(self, repository: ComercioRepository):
        self.repository = repository

    def register_comercio(self, data: ComercioCreate) -> Dict[str, Any]:
        if self.repository.exists_by_name_and_address(data.name, data.address):
            raise LookupError("A business with that name and address already exists.")

        comercio = Comercio(
            name=data.name,
            address=data.address,
            category=data.category,
            phone=data.phone,
            email=data.email,
        )
        self.repository.save(comercio)

        return {
            "message": "Business registered successfully. Pending approval.",
            "data": {
                "merchant_id": comercio.merchant_id,
                "name": comercio.name,
                "status": comercio.status,
            },
            "success": True,
        }


comercio_service = ComercioService(comercio_repository)
