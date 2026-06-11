from mi_api.Repartidor.domain.dealer_domain import (
    DealerCreate, DealerResponseData, DealerAvailabilityResponseData,
)
from mi_api.Repartidor.repository.dealer_repository import DealerRepository


class DealerService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def register(self, data: DealerCreate) -> DealerResponseData:
        if self.repo.find_by_email(data.email) or self.repo.find_by_license(data.license_number):
            raise ValueError("Email or license number is already registered.")

        dealer = self.repo.create(
            full_name=data.full_name,
            phone=data.phone,
            email=data.email,
            vehicle_type=data.vehicle_type,
            license_number=data.license_number,
        )

        print(f"[EMAIL NOTIFICATION] Confirmation email sent to {dealer.email}")

        return DealerResponseData(**dealer.to_dict())

    def confirm_dealer(self, dealer_id: str) -> DealerResponseData:
        dealer = self.repo.find_by_id(dealer_id)
        if not dealer:
            raise LookupError("Dealer not found.")
        if dealer.account_status != "pending_activation":
            raise ValueError("Only dealers in pending_activation status can be confirmed.")
        updated = self.repo.update_account_status(dealer_id, "active")
        self.repo.update_availability(dealer_id, "available")
        return DealerResponseData(**updated.to_dict())

    def toggle_availability(self, dealer_id: str) -> DealerAvailabilityResponseData:
        dealer = self.repo.find_by_id(dealer_id)
        if not dealer:
            raise LookupError("Driver not found.")
        if dealer.account_status != "active":
            raise ValueError("Availability can only be toggled for active dealers.")
        if self.repo.find_active_order_by_dealer_id(dealer_id) is not None:
            raise ValueError("Cannot change availability while you have an active order assigned.")
        new_status = "unavailable" if dealer.availability == "available" else "available"
        self.repo.update_availability(dealer_id, new_status)
        return DealerAvailabilityResponseData(dealer_id=dealer.dealer_id, status=new_status)
