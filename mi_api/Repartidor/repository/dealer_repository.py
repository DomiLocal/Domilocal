# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — Repartidor/repository/dealer_repository.py
# ─────────────────────────────────────────────────────────────
from typing import Optional
import uuid
from domain.dealer_domain import Dealer

Dealer.latitude = 0.0
Dealer.longitude = 0.0

class DealerRepository:
    def __init__(self):
        self._dealers: list[Dealer] = []
        self._assigned_orders: set[str] = set()
        self._pending_assignments: dict[str, str] = {}  # order_id -> dealer_id
        self._seed()

    def _seed(self):
        """Datos base estables para pruebas."""
        carlos = Dealer(
            dealer_id="R-00123",
            full_name="Carlos Pérez",
            phone="3001234567",
            email="test@example.com",
            vehicle_type="moto",
            license_number="LIC-12345",
            status="available"
        )
        carlos.latitude = 7.121
        carlos.longitude = -73.121
        self._dealers.append(carlos)

        juan = Dealer(
            dealer_id="R-00555",
            full_name="Juan Rodríguez",
            phone="3159876543",
            email="juan.reparto@example.com",
            vehicle_type="bicycle",
            license_number="LIC-99999",
            status="available"
        )
        juan.latitude = 7.135
        juan.longitude = -73.135
        self._dealers.append(juan)

    def find_by_email(self, email: str) -> Optional[Dealer]:
        return next((d for d in self._dealers if d.email.lower() == email.lower()), None)

    def find_by_license(self, license_number: str) -> Optional[Dealer]:
        return next((d for d in self._dealers if d.license_number == license_number), None)

    def create(self, full_name: str, phone: str, email: str, 
               vehicle_type: str, license_number: str) -> Dealer:
        short_id = str(uuid.uuid4()).split("-")[0].upper()
        dealer_id = f"R-{short_id[:5]}"
        new_dealer = Dealer(
            dealer_id=dealer_id, full_name=full_name, phone=phone,
            email=email, vehicle_type=vehicle_type, license_number=license_number,
            status="pending_activation"
        )
        new_dealer.latitude = 7.122
        new_dealer.longitude = -73.122
        self._dealers.append(new_dealer)
        return new_dealer

    def find_available_dealers(self, exclude_ids: Optional[set] = None) -> list[Dealer]:
        excluded = exclude_ids or set()
        return [d for d in self._dealers if d.status == "available" and d.dealer_id not in excluded]

    def update_status(self, dealer_id: str, new_status: str) -> Optional[Dealer]:
        for d in self._dealers:
            if d.dealer_id == dealer_id:
                d.status = new_status
                return d
        return None

    def is_order_already_assigned(self, order_id: str) -> bool:
        return order_id in self._assigned_orders

    def lock_order(self, order_id: str):
        self._assigned_orders.add(order_id)

    def unlock_order(self, order_id: str):
        self._assigned_orders.discard(order_id)

    def record_pending_assignment(self, order_id: str, dealer_id: str):
        self._pending_assignments[order_id] = dealer_id

    def get_pending_assignment_dealer(self, order_id: str) -> Optional[str]:
        return self._pending_assignments.get(order_id)

    def clear_pending_assignment(self, order_id: str):
        self._pending_assignments.pop(order_id, None)

# Creamos una única instancia aquí que se compartirá globalmente a través de FastAPI
_global_repo_instance = DealerRepository()

def get_dealer_repository() -> DealerRepository:
    """Función proveedora de la dependencia para FastAPI."""
    return _global_repo_instance