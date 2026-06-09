# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — Repartidor/repository/dealer_repository.py
# ─────────────────────────────────────────────────────────────
from typing import Optional
import urllib.parse
import uuid
from domain.dealer_domain import Dealer
from domain.dealer_delivery_domain import Order
from domain.dealer_active_order_domain import (
    ActiveOrderDetail, Merchant, Customer, Product
)

Dealer.latitude = 0.0
Dealer.longitude = 0.0

class DealerRepository:
    def __init__(self):
        self._dealers: list[Dealer] = []
        self._assigned_orders: set[str] = set()
        self._pending_assignments: dict[str, str] = {}
        self._orders: dict[str, Order] = {}
        self._active_order_details: dict[str, ActiveOrderDetail] = {}
        self._seed()
        self._seed_orders()
        self._seed_active_order_details()

    def _seed(self):
        carlos = Dealer(
            dealer_id="R-00123",
            full_name="Carlos Pérez",
            phone="3001234567",
            email="test@example.com",
            vehicle_type="moto",
            license_number="LIC-12345",
            account_status="active",
            availability="available"
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
            account_status="active",
            availability="available"
        )
        juan.latitude = 7.135
        juan.longitude = -73.135
        self._dealers.append(juan)

    def _seed_orders(self):
        # PED-0456 en tránsito, asignado a Carlos → Carlos queda unavailable
        self._orders["PED-0456"] = Order("PED-0456", "in_transit", "R-00123")
        self.update_availability("R-00123", "unavailable")

        # Pedidos en estado incorrecto para pruebas del Caso 2
        self._orders["PED-RECEIVED-001"] = Order("PED-RECEIVED-001", "received")
        self._orders["PED-PREP-001"] = Order("PED-PREP-001", "in_preparation")

    def find_by_id(self, dealer_id: str) -> Optional[Dealer]:
        return next((d for d in self._dealers if d.dealer_id == dealer_id), None)

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
            account_status="pending_activation",
            availability=None
        )
        new_dealer.latitude = 7.122
        new_dealer.longitude = -73.122
        self._dealers.append(new_dealer)
        return new_dealer

    def find_available_dealers(self, exclude_ids: Optional[set] = None) -> list[Dealer]:
        excluded = exclude_ids or set()
        return [
            d for d in self._dealers
            if d.account_status == "active"
            and d.availability == "available"
            and d.dealer_id not in excluded
        ]

    def update_account_status(self, dealer_id: str, account_status: str) -> Optional[Dealer]:
        for d in self._dealers:
            if d.dealer_id == dealer_id:
                d.account_status = account_status
                return d
        return None

    def update_availability(self, dealer_id: str, availability: str) -> Optional[Dealer]:
        for d in self._dealers:
            if d.dealer_id == dealer_id:
                d.availability = availability
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

    def _seed_active_order_details(self):
        address = "Carrera 10 #45-20, Apto 301"
        map_link = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(address)
        self._active_order_details["PED-0456"] = ActiveOrderDetail(
            order_id="PED-0456",
            merchant=Merchant(name="Tienda La Esquina", address="Calle 5 #12-30, Bucaramanga"),
            customer=Customer(
                name="Ana Gómez",
                phone="3001234567",
                delivery_address=address,
                map_link=map_link,
                notes="Dejar en portería si no hay respuesta",
            ),
            products=[
                Product(name="Agua 500ml", quantity=2),
                Product(name="Pan tajado", quantity=1),
            ],
        )

    # ── Métodos de Órdenes (HU-C03) ──────────────────────────
    def find_order_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def create_order(self, order_id: str, status: str, dealer_id: Optional[str] = None) -> Order:
        order = Order(order_id, status, dealer_id)
        self._orders[order_id] = order
        return order

    def update_order_status(self, order_id: str, status: str, delivery_time=None) -> Optional[Order]:
        order = self._orders.get(order_id)
        if order:
            order.status = status
            if delivery_time is not None:
                order.delivery_time = delivery_time
        return order

    # ── Métodos de pedido activo (HU-C05) ────────────────────
    def find_active_order_by_dealer_id(self, dealer_id: str) -> Optional[ActiveOrderDetail]:
        active_statuses = {"received", "in_preparation", "in_transit"}
        for order in self._orders.values():
            if order.dealer_id == dealer_id and order.status in active_statuses:
                return self._active_order_details.get(order.order_id)
        return None

    def create_active_order_detail(
        self,
        order_id: str,
        merchant: Merchant,
        customer: Customer,
        products: list[Product],
    ) -> ActiveOrderDetail:
        detail = ActiveOrderDetail(order_id, merchant, customer, products)
        self._active_order_details[order_id] = detail
        return detail


_global_repo_instance = DealerRepository()

def get_dealer_repository() -> DealerRepository:
    """Función proveedora de la dependencia para FastAPI."""
    return _global_repo_instance
