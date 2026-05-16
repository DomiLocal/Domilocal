from typing import List, Optional
from domain.models import DeliveryPerson, DeliveryStatus
from repository.delivery_repo import delivery_repo
from fastapi import HTTPException

class DeliveryService:
    def register_repartidor(self, dp: DeliveryPerson) -> DeliveryPerson:
        if delivery_repo.get_by_email_or_license(dp.correo, dp.nro_licencia):
            raise HTTPException(status_code=409, detail="El correo o número de licencia ya se encuentra registrado.")
            
        if not any(char.isdigit() for char in dp.password):
            raise HTTPException(status_code=400, detail="La contraseña debe incluir al menos un número.")
            
        dp.estado = DeliveryStatus.PENDIENTE
        return delivery_repo.create(dp)

    def update_availability(self, dp_id: str, status: DeliveryStatus) -> DeliveryPerson:
        res = delivery_repo.update_availability(dp_id, status)
        if not res:
            raise HTTPException(status_code=404, detail="Repartidor no encontrado.")
        return res

    def get_available_repartidor(self) -> Optional[DeliveryPerson]:
        return delivery_repo.get_available_nearest()

delivery_service = DeliveryService()
