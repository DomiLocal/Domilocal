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


comercio_repository = ComercioRepository()
