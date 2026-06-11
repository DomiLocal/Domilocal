MERCHANTS: dict = {}
PRODUCTS: dict = {}
ORDERS: dict = {}

_order_counter = {"value": 1}


def next_order_id() -> str:
    oid = f"PED-{_order_counter['value']:05d}"
    _order_counter["value"] += 1
    return oid
