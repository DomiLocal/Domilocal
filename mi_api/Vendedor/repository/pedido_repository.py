from domain.pedido import Pedido, EstadoPedido
from repository.shared_store import ORDERS


class RepositorioPedido:

    def obtener_por_id(self, id_pedido: str):
        data = ORDERS.get(id_pedido)
        if not data:
            return None
        return Pedido(
            id_pedido=data["order_id"],
            estado=EstadoPedido(data["status"]),
            fecha_actualizacion=data.get("updated_at"),
        )

    def guardar(self, pedido: Pedido):
        if pedido.id_pedido in ORDERS:
            ORDERS[pedido.id_pedido]["status"] = pedido.estado.value
            ORDERS[pedido.id_pedido]["updated_at"] = pedido.fecha_actualizacion
        return pedido


repositorio_pedido = RepositorioPedido()
