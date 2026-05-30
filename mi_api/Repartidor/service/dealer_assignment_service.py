# ─────────────────────────────────────────────────────────────
# CAPA SERVICIO (HU2) — Repartidor/service/dealer_assignment_service.py
# ─────────────────────────────────────────────────────────────
import math
from typing import Optional
from domain.dealer_assignment_domain import AssignmentResponseData
from repository.dealer_repository import DealerRepository

class DealerAssignmentService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def assign_closest_dealer(self, order_id: str, store_lat: float, store_lng: float) -> Optional[AssignmentResponseData]:
        # 1. BLOQUEO ABSOLUTO: Si el ID de la orden ya está registrado, lanzar excepción de negocio
        if self.repo.is_order_already_assigned(order_id):
            raise ValueError(f"Order {order_id} has already been assigned to a dealer.")

        # 2. Buscar repartidores disponibles
        candidates = self.repo.find_available_dealers()
        if not candidates:
            return None

        # 3. Encontrar el más cercano
        closest_dealer = min(
            candidates,
            key=lambda d: self.calculate_distance(store_lat, store_lng, d.latitude, d.longitude)
        )

        # 4. Actualizar estados sincronizadamente en el repositorio central
        self.repo.update_status(closest_dealer.dealer_id, "assigned")
        self.repo.lock_order(order_id)

        print(f"[NOTIFICATION] Push notification sent to Dealer {closest_dealer.dealer_id}")

        return AssignmentResponseData(
            order_id=order_id,
            dealer_id=closest_dealer.dealer_id,
            dealer_name=closest_dealer.full_name,
            acceptance_timeout_seconds=60
        )