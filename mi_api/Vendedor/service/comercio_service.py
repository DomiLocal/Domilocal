from typing import Dict, Any, Optional
from domain.comercio_domain import ComercioCreate, Comercio
from repository.comercio_repository import ComercioRepository, comercio_repository

ALLOWED_STATUSES = {"active", "inactive"}


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

    def get_by_id(self, merchant_id: str) -> Optional[Dict]:
        return self.repository.get_by_id(merchant_id)

    def update_status(self, merchant_id: str, new_status: str) -> Dict[str, Any]:
        merchant = self.repository.get_by_id(merchant_id)
        if not merchant:
            raise LookupError("Merchant not found.")
        if new_status not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status. Allowed values: {', '.join(ALLOWED_STATUSES)}.")
        if merchant["status"] == "pending_approval":
            raise ValueError("Cannot change status of a merchant pending approval.")

        self.repository.update_status(merchant_id, new_status)

        return {
            "message": "Business status updated successfully.",
            "data": {
                "merchant_id": merchant_id,
                "name": merchant["name"],
                "status": new_status,
            },
            "success": True,
        }


comercio_service = ComercioService(comercio_repository)
