from typing import Optional, Dict
from domain.comercio_domain import Comercio
from repository.shared_store import MERCHANTS


class ComercioRepository:

    def exists_by_name_and_address(self, name: str, address: str) -> bool:
        return any(
            m["name"].lower() == name.lower() and m["address"].lower() == address.lower()
            for m in MERCHANTS.values()
        )

    def save(self, comercio: Comercio) -> Comercio:
        MERCHANTS[comercio.merchant_id] = comercio.to_dict()
        return comercio

    def get_by_id(self, merchant_id: str) -> Optional[Dict]:
        return MERCHANTS.get(merchant_id)

    def update_status(self, merchant_id: str, new_status: str) -> None:
        if merchant_id in MERCHANTS:
            MERCHANTS[merchant_id]["status"] = new_status


comercio_repository = ComercioRepository()
