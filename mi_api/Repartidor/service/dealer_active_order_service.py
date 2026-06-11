from mi_api.Repartidor.domain.dealer_active_order_domain import ActiveOrderDetail
from mi_api.Repartidor.repository.dealer_repository import DealerRepository


class DealerActiveOrderService:
    def __init__(self, repo: DealerRepository):
        self.repo = repo

    def get_active_order(self, dealer_id: str) -> tuple[ActiveOrderDetail | None, str]:
        dealer = self.repo.find_by_id(dealer_id)
        if dealer is None:
            return None, "dealer_not_found"

        detail = self.repo.find_active_order_by_dealer_id(dealer_id)
        if detail is None:
            return None, "no_active_order"

        return detail, "ok"
