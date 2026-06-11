import math
import urllib.parse
from typing import Optional

from mi_api.Repartidor.domain.dealer_assignment_domain import AssignmentResponseData
from mi_api.Repartidor.domain.dealer_active_order_domain import ActiveOrderDetail, Merchant, Customer, Product
from mi_api.Repartidor.repository.dealer_repository import DealerRepository
from mi_api.shared_store import ORDERS, MERCHANTS


class DealerAssignmentService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def assign_closest_dealer(
        self, order_id: str, store_lat: float, store_lng: float, exclude_ids: Optional[set] = None
    ) -> Optional[AssignmentResponseData]:
        order_data = ORDERS.get(order_id)
        if not order_data:
            raise ValueError(f"Order '{order_id}' not found.")
        if order_data.get("status") != "ready_for_pickup":
            raise ValueError(
                f"Order '{order_id}' cannot be assigned a dealer. "
                "It must be in 'ready_for_pickup' status first."
            )
        if self.repo.is_order_already_assigned(order_id):
            raise ValueError(f"Order {order_id} has already been assigned to a dealer.")

        candidates = self.repo.find_available_dealers(exclude_ids=exclude_ids)
        if not candidates:
            return None

        closest_dealer = min(
            candidates,
            key=lambda d: self.calculate_distance(store_lat, store_lng, d.latitude, d.longitude),
        )

        self.repo.update_availability(closest_dealer.dealer_id, "unavailable")
        self.repo.lock_order(order_id)
        self.repo.record_pending_assignment(order_id, closest_dealer.dealer_id)
        self.repo.create_order(order_id, "in_transit", closest_dealer.dealer_id)
        self._build_active_order_detail(order_id, closest_dealer.dealer_id)

        print(f"[NOTIFICATION] Push notification sent to Dealer {closest_dealer.dealer_id}")

        return AssignmentResponseData(
            order_id=order_id,
            dealer_id=closest_dealer.dealer_id,
            dealer_name=closest_dealer.full_name,
            acceptance_timeout_seconds=60,
        )

    def _build_active_order_detail(self, order_id: str, dealer_id: str) -> None:
        order_data = ORDERS.get(order_id, {})
        address = order_data.get("delivery_address", "Dirección pendiente")
        merchant_id = order_data.get("merchant_id", "")
        merchant_data = MERCHANTS.get(merchant_id, {})
        map_link = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(address)

        self.repo.create_active_order_detail(
            order_id=order_id,
            merchant=Merchant(
                name=merchant_data.get("name", "Comercio asignado"),
                address=merchant_data.get("address", "Dirección del comercio pendiente"),
            ),
            customer=Customer(
                name=order_data.get("customer", "Cliente del pedido"),
                phone=order_data.get("customer_phone", "Sin teléfono registrado"),
                delivery_address=address,
                map_link=map_link,
                notes=order_data.get("notes"),
            ),
            products=[
                Product(name=p["name"], quantity=p["quantity"])
                for p in order_data.get("products", [{"name": f"Productos de {order_id}", "quantity": 1}])
            ],
        )

    def reassign_after_timeout(
        self, order_id: str, original_dealer_id: str, store_lat: float, store_lng: float
    ) -> Optional[AssignmentResponseData]:
        if self.repo.get_pending_assignment_dealer(order_id) != original_dealer_id:
            return None

        self.repo.update_availability(original_dealer_id, "available")
        self.repo.clear_pending_assignment(order_id)
        self.repo.unlock_order(order_id)

        print(f"[TIMEOUT] Dealer {original_dealer_id} did not accept. Reassigning order {order_id}...")

        return self.assign_closest_dealer(order_id, store_lat, store_lng, exclude_ids={original_dealer_id})
