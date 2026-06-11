from typing import Optional
import urllib.parse
import uuid
from datetime import datetime

from mi_api.Repartidor.domain.dealer_domain import Dealer
from mi_api.Repartidor.domain.dealer_active_order_domain import (
    ActiveOrderDetail, Merchant, Customer, Product,
)
from mi_api.shared_store import ORDERS, MERCHANTS


class DealerRepository:
    def __init__(self):
        self._dealers: list[Dealer] = []
        self._assigned_orders: set[str] = set()
        self._pending_assignments: dict[str, str] = {}
        self._active_order_details: dict[str, ActiveOrderDetail] = {}
        self._seed()

    # ── Seeding ───────────────────────────────────────────────
    def _seed(self):
        carlos = Dealer(
            dealer_id="R-00123",
            full_name="Carlos Pérez",
            phone="3001234567",
            email="carlos@domilocal.com",
            vehicle_type="moto",
            license_number="LIC-12345",
            account_status="active",
            availability="available",
        )
        carlos.latitude = 7.121
        carlos.longitude = -73.121
        self._dealers.append(carlos)

        juan = Dealer(
            dealer_id="R-00555",
            full_name="Juan Rodríguez",
            phone="3159876543",
            email="juan.reparto@domilocal.com",
            vehicle_type="bicycle",
            license_number="LIC-99999",
            account_status="active",
            availability="available",
        )
        juan.latitude = 7.135
        juan.longitude = -73.135
        self._dealers.append(juan)

    # ── Dealer CRUD ───────────────────────────────────────────
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
            dealer_id=dealer_id,
            full_name=full_name,
            phone=phone,
            email=email,
            vehicle_type=vehicle_type,
            license_number=license_number,
            account_status="pending_activation",
            availability=None,
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

    # ── Order locking ─────────────────────────────────────────
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

    # ── Order operations (via shared ORDERS) ──────────────────
    def find_order_by_id(self, order_id: str):
        data = ORDERS.get(order_id)
        if not data:
            return None
        from mi_api.Repartidor.domain.dealer_delivery_domain import Order as DeliveryOrder
        order = DeliveryOrder(
            order_id=data["order_id"],
            status=data["status"],
            dealer_id=data.get("dealer_id"),
        )
        order.delivery_time = data.get("delivery_time")
        return order

    def create_order(self, order_id: str, status: str, dealer_id: Optional[str] = None):
        if order_id not in ORDERS:
            ORDERS[order_id] = {
                "order_id": order_id,
                "merchant_id": "",
                "customer": "Cliente",
                "client_id": None,
                "status": status,
                "total": 0.0,
                "items": [],
                "products": [],
                "delivery_address": "",
                "payment_method": "cash",
                "dealer_id": dealer_id,
                "dealer": None,
                "notes": None,
                "status_history": [{"status": status, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}],
                "created_at": datetime.utcnow(),
                "updated_at": None,
                "delivery_time": None,
            }
        else:
            ORDERS[order_id]["status"] = status
            ORDERS[order_id]["dealer_id"] = dealer_id
            ORDERS[order_id]["updated_at"] = datetime.utcnow()
            if dealer_id:
                # Update dealer info for Client status view
                dealer = self.find_by_id(dealer_id)
                if dealer:
                    ORDERS[order_id]["dealer"] = {"name": dealer.full_name, "phone": dealer.phone}
        return self.find_order_by_id(order_id)

    def update_order_status(self, order_id: str, status: str, delivery_time=None):
        data = ORDERS.get(order_id)
        if data:
            data["status"] = status
            data["updated_at"] = datetime.utcnow()
            if delivery_time is not None:
                data["delivery_time"] = delivery_time
            data["status_history"].append(
                {"status": status, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
            )
        return self.find_order_by_id(order_id)

    # ── Active order (HU-C05) ─────────────────────────────────
    def find_active_order_by_dealer_id(self, dealer_id: str) -> Optional[ActiveOrderDetail]:
        active_statuses = {"received", "in_preparation", "in_transit", "ready_for_pickup"}
        for order_id, data in ORDERS.items():
            if data.get("dealer_id") == dealer_id and data.get("status") in active_statuses:
                # Return cached detail if available, else build from ORDERS
                if order_id in self._active_order_details:
                    return self._active_order_details[order_id]
                return self._build_active_order_detail(order_id, data)
        return None

    def _build_active_order_detail(self, order_id: str, data: dict) -> ActiveOrderDetail:
        address = data.get("delivery_address", "Dirección pendiente")
        merchant_id = data.get("merchant_id", "")
        merchant_data = MERCHANTS.get(merchant_id, {})
        map_link = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(address)
        return ActiveOrderDetail(
            order_id=order_id,
            merchant=Merchant(
                name=merchant_data.get("name", "Comercio"),
                address=merchant_data.get("address", ""),
            ),
            customer=Customer(
                name=data.get("customer", "Cliente"),
                phone=data.get("customer_phone", "Sin teléfono"),
                delivery_address=address,
                map_link=map_link,
                notes=data.get("notes"),
            ),
            products=[
                Product(name=p["name"], quantity=p["quantity"])
                for p in data.get("products", [])
            ],
        )

    def create_active_order_detail(
        self, order_id: str, merchant, customer, products: list
    ) -> ActiveOrderDetail:
        detail = ActiveOrderDetail(order_id, merchant, customer, products)
        self._active_order_details[order_id] = detail
        return detail


_global_repo_instance = DealerRepository()


def get_dealer_repository() -> DealerRepository:
    return _global_repo_instance
