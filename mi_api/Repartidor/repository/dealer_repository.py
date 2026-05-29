# ─────────────────────────────────────────────────────────────
# CAPA REPOSITORIO — Repartidor/repository/dealer_repository.py
# ─────────────────────────────────────────────────────────────
from typing import Optional
import uuid
from domain.dealer_domain import Dealer

class DealerRepository:
    def __init__(self):
        # Almacén en memoria usando objetos de dominio
        self._dealers: list[Dealer] = []
        self._seed()

    def _seed(self):
        """Datos iniciales de prueba para validar duplicados (Caso 2)."""
        self._dealers.append(
            Dealer(
                dealer_id="R-00123",
                full_name="Carlos Pérez",
                phone="3001234567",
                email="test@example.com",
                vehicle_type="moto",
                license_number="LIC-12345"
            )
        )

    def find_by_email(self, email: str) -> Optional[Dealer]:
        return next((d for d in self._dealers if d.email.lower() == email.lower()), None)

    def find_by_license(self, license_number: str) -> Optional[Dealer]:
        return next((d for d in self._dealers if d.license_number == license_number), None)

    def create(self, full_name: str, phone: str, email: str, 
               vehicle_type: str, license_number: str) -> Dealer:
        # Generar ID formateado como pide el issue
        short_id = str(uuid.uuid4()).split("-")[0].upper()
        dealer_id = f"R-{short_id[:5]}"
        
        new_dealer = Dealer(
            dealer_id=dealer_id,
            full_name=full_name,
            phone=phone,
            email=email,
            vehicle_type=vehicle_type,
            license_number=license_number,
            status="pending_activation"
        )
        self._dealers.append(new_dealer)
        return new_dealer

# Instancia compartida (Singleton)
dealer_repository = DealerRepository()