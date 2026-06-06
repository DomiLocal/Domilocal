# ─────────────────────────────────────────────────────────────
# CAPA SERVICIO — Repartidor/service/dealer_service.py
# ─────────────────────────────────────────────────────────────
from domain.dealer_domain import DealerCreate, DealerResponseData, DealerAvailabilityResponseData
from repository.dealer_repository import DealerRepository

class DealerService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def register(self, data: DealerCreate) -> DealerResponseData:
        # REGLA DE NEGOCIO: Validar duplicados de email o licencia (Caso 2)
        if self.repo.find_by_email(data.email) or self.repo.find_by_license(data.license_number):
            raise ValueError("Email or license number is already registered.")

        # Guardar a través del repositorio
        dealer = self.repo.create(
            full_name=data.full_name,
            phone=data.phone,
            email=data.email,
            vehicle_type=data.vehicle_type,
            license_number=data.license_number
        )

        # Envío de correo simulado (Criterio de aceptación 2)
        print(f"[EMAIL NOTIFICATION] Confirmation email sent to {dealer.email}")

        return DealerResponseData(**dealer.to_dict())

    def confirm_dealer(self, dealer_id: str) -> DealerResponseData:
        dealer = self.repo.find_by_id(dealer_id)
        if not dealer:
            raise LookupError("Dealer not found.")
        if dealer.account_status != "pending_activation":
            raise ValueError("Only dealers in pending_activation status can be confirmed.")
        updated = self.repo.update_account_status(dealer_id, "active")
        return DealerResponseData(**updated.to_dict())

    def toggle_availability(self, dealer_id: str) -> DealerAvailabilityResponseData:
        dealer = self.repo.find_by_id(dealer_id)
        if not dealer:
            raise LookupError("Driver not found.")
        if dealer.account_status != "active":
            raise ValueError("Availability can only be toggled for active dealers.")
        new_status = "unavailable" if dealer.availability == "available" else "available"
        self.repo.update_availability(dealer_id, new_status)
        return DealerAvailabilityResponseData(dealer_id=dealer.dealer_id, status=new_status)
