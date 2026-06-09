# ─────────────────────────────────────────────────────────────
# CAPA SERVICIO (HU2) — Repartidor/service/dealer_assignment_service.py
# ─────────────────────────────────────────────────────────────
import math
import urllib.parse
from typing import Optional
from domain.dealer_assignment_domain import AssignmentResponseData
from domain.dealer_active_order_domain import ActiveOrderDetail, Merchant, Customer, Product
from repository.dealer_repository import DealerRepository

class DealerAssignmentService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def assign_closest_dealer(self, order_id: str, store_lat: float, store_lng: float, exclude_ids: Optional[set] = None) -> Optional[AssignmentResponseData]:
        if self.repo.is_order_already_assigned(order_id):
            raise ValueError(f"Order {order_id} has already been assigned to a dealer.")

        candidates = self.repo.find_available_dealers(exclude_ids=exclude_ids)
        if not candidates:
            return None

        closest_dealer = min(
            candidates,
            key=lambda d: self.calculate_distance(store_lat, store_lng, d.latitude, d.longitude)
        )

        self.repo.update_availability(closest_dealer.dealer_id, "unavailable")
        self.repo.lock_order(order_id)
        self.repo.record_pending_assignment(order_id, closest_dealer.dealer_id)
        self.repo.create_order(order_id, "in_transit", closest_dealer.dealer_id)
        self._create_placeholder_detail(order_id)

        print(f"[NOTIFICATION] Push notification sent to Dealer {closest_dealer.dealer_id}")

        return AssignmentResponseData(
            order_id=order_id,
            dealer_id=closest_dealer.dealer_id,
            dealer_name=closest_dealer.full_name,
            acceptance_timeout_seconds=60
        )

    def _create_placeholder_detail(self, order_id: str) -> None:
        delivery_address = "Dirección de entrega pendiente de confirmar"
        map_link = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(delivery_address)
        self.repo.create_active_order_detail(
            order_id=order_id,
            merchant=Merchant(name="Comercio asignado", address="Dirección del comercio pendiente"),
            customer=Customer(
                name="Cliente del pedido",
                phone="Sin teléfono registrado",
                delivery_address=delivery_address,
                map_link=map_link,
                notes=None,
            ),
            products=[Product(name=f"Productos de {order_id}", quantity=1)],
        )

    def reassign_after_timeout(self, order_id: str, original_dealer_id: str, store_lat: float, store_lng: float) -> Optional[AssignmentResponseData]:
        if self.repo.get_pending_assignment_dealer(order_id) != original_dealer_id:
            return None  # Ya fue aceptado; no hay nada que hacer

        self.repo.update_availability(original_dealer_id, "available")
        self.repo.clear_pending_assignment(order_id)
        self.repo.unlock_order(order_id)

        print(f"[TIMEOUT] Dealer {original_dealer_id} no aceptó. Reasignando orden {order_id}...")

        return self.assign_closest_dealer(order_id, store_lat, store_lng, exclude_ids={original_dealer_id})
