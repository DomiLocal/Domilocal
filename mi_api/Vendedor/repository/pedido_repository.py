from domain.pedido import Pedido, EstadoPedido


class RepositorioPedido:

    def __init__(self):
        self._pedidos = {
            "PED-0789": Pedido(
                id_pedido="PED-0789",
                estado=EstadoPedido.EN_PREPARACION
            )
        }

    def obtener_por_id(self, id_pedido: str):
        return self._pedidos.get(id_pedido)

    def guardar(self, pedido: Pedido):
        self._pedidos[pedido.id_pedido] = pedido
        return pedido


repositorio_pedido = RepositorioPedido()
