from typing import List, Optional
from domain.models import DeliveryPerson, DeliveryStatus

class DeliveryRepository:
    def __init__(self):
        self._repartidores: List[DeliveryPerson] = []
        self._counter = 1

    def create(self, dp: DeliveryPerson) -> DeliveryPerson:
        dp.id_repartidor = f"R-{self._counter:05d}"
        self._repartidores.append(dp)
        self._counter += 1
        return dp

    def get_by_email_or_license(self, email: str, license: str) -> Optional[DeliveryPerson]:
        return next((r for r in self._repartidores if r.correo == email or r.nro_licencia == license), None)

    def get_by_id(self, dp_id: str) -> Optional[DeliveryPerson]:
        return next((r for r in self._repartidores if r.id_repartidor == dp_id), None)

    def update_availability(self, dp_id: str, status: DeliveryStatus) -> Optional[DeliveryPerson]:
        dp = self.get_by_id(dp_id)
        if dp:
            dp.estado = status
            return dp
        return None

    def get_available_nearest(self) -> Optional[DeliveryPerson]:
        # Simulating nearest by picking the first available
        return next((r for r in self._repartidores if r.estado == DeliveryStatus.DISPONIBLE), None)

delivery_repo = DeliveryRepository()
