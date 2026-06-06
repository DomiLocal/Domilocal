# ─────────────────────────────────────
# REPOSITORY LAYER
# Database simulation
# ─────────────────────────────────────

from domain.comercio import Merchant


class MerchantRepository:

    def __init__(self):
        self._merchants = []
        self._counter = 1

    def get_by_name_address(
        self,
        name,
        address
    ):
        return next(
            (
                m for m in self._merchants
                if m.name.lower() == name.lower()
                and
                m.address.lower() == address.lower()
            ),
            None
        )

    def create(self, data):
        new_merchant = Merchant(
            id_merchant=f"MER-{self._counter:03}",
            name=data.name,
            address=data.address,
            category=data.category,
            phone=data.phone,
            contact_email=data.contact_email,
            status="pending_approval"
        )

        self._merchants.append(
            new_merchant
        )

        self._counter += 1

        return new_merchant


merchant_repository = MerchantRepository()
