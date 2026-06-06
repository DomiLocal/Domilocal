from datetime import datetime
from typing import Optional


class Order:

    def __init__(
        self,
        order_id: str,
        status: str,
        updated_at: Optional[str] = None
    ):
        self.order_id = order_id
        self.status = status
        self.updated_at = updated_at

    def mark_as_ready_for_pickup(self) -> None:
        """
        Transitions order status from 'in_preparation' to 'ready_for_pickup'.
        """
        if self.status != "in_preparation":
            raise ValueError(
                "Unable to update status. The order is not in preparation."
            )

        self.status = "ready_for_pickup"
        # Register exact ISO format UTC datetime
        self.updated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "status": self.status,
            "updated_at": self.updated_at
        }
