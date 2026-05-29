# ─────────────────────────────────────────────────────────────
# CAPA SERVICIO — Repartidor/service/dealer_service.py
# ─────────────────────────────────────────────────────────────
from domain.dealer_domain import DealerCreate, DealerResponseData
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