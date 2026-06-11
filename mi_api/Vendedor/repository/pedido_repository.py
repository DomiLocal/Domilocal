from mi_api.Vendedor.domain.pedido import Pedido, EstadoPedido
from mi_api.shared_store import ORDERS


class RepositorioPedido:

    def obtener_por_id(self, id_pedido: str):
        data = ORDERS.get(id_pedido)
        if not data:
            return None
        try:
            estado = EstadoPedido(data["status"])
        except ValueError:
            # Status exists but is not in the Vendedor-managed states
            # (e.g. in_transit, delivered) — treat as not found for this module
            return None
        return Pedido(
            id_pedido=data["order_id"],
            estado=estado,
            fecha_actualizacion=data.get("updated_at"),
        )

    def guardar(self, pedido: Pedido):
        if pedido.id_pedido in ORDERS:
            ORDERS[pedido.id_pedido]["status"] = pedido.estado.value
            ORDERS[pedido.id_pedido]["updated_at"] = pedido.fecha_actualizacion
            # Add status history entry
            if ORDERS[pedido.id_pedido].get("status_history") is not None:
                from datetime import datetime
                ORDERS[pedido.id_pedido]["status_history"].append(
                    {"status": pedido.estado.value, "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
                )
        return pedido


repositorio_pedido = RepositorioPedido()
