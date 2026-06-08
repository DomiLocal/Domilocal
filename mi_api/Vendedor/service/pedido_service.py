from domain.pedido import PedidoRespuesta
from repository.pedido_repository import RepositorioPedido


class ServicioPedido:

    def __init__(self, repositorio: RepositorioPedido):
        self.repositorio = repositorio

    def marcar_listo_para_recoger(self, id_pedido: str):

        pedido = self.repositorio.obtener_por_id(id_pedido)

        if not pedido:
            raise LookupError("Order not found")

        pedido.marcar_listo_para_recoger()

        self.repositorio.guardar(pedido)

        self.notificar_modulo_repartidores(id_pedido)
        self.notificar_cliente(id_pedido)

        return PedidoRespuesta(**pedido.a_respuesta())

    def notificar_modulo_repartidores(self, id_pedido: str):
        print(
            f"[EVENT] Order {id_pedido} sent to delivery assignment module"
        )

    def notificar_cliente(self, id_pedido: str):
        print(
            f"[EVENT] Customer notified: order {id_pedido} ready for pickup"
        )
