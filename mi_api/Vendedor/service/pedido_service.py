from mi_api.Vendedor.domain.pedido import PedidoRespuesta
from mi_api.Vendedor.repository.pedido_repository import RepositorioPedido


class ServicioPedido:

    def __init__(self, repositorio: RepositorioPedido):
        self.repositorio = repositorio

    def marcar_listo_para_recoger(self, id_pedido: str):
        pedido = self.repositorio.obtener_por_id(id_pedido)

        if not pedido:
            raise LookupError("Order not found")

        pedido.marcar_listo_para_recoger()
        self.repositorio.guardar(pedido)

        # Trigger automatic dealer assignment
        self._notificar_y_asignar_repartidor(id_pedido)
        self.notificar_cliente(id_pedido)

        return PedidoRespuesta(**pedido.a_respuesta())

    def _notificar_y_asignar_repartidor(self, id_pedido: str):
        print(f"[EVENT] Order {id_pedido} sent to delivery assignment module")
        try:
            from mi_api.Repartidor.repository.dealer_repository import get_dealer_repository
            from mi_api.Repartidor.service.dealer_assignment_service import DealerAssignmentService

            repo = get_dealer_repository()
            service = DealerAssignmentService(repo=repo)
            STORE_LAT = 7.120
            STORE_LNG = -73.120
            result = service.assign_closest_dealer(id_pedido, STORE_LAT, STORE_LNG)
            if result:
                print(f"[EVENT] Dealer {result.dealer_id} assigned to order {id_pedido}")
            else:
                print(f"[EVENT] No dealers available for order {id_pedido}, will retry.")
        except ValueError as e:
            # Already assigned or other business rule violation — log and continue
            print(f"[WARN] Could not auto-assign dealer for {id_pedido}: {e}")
        except Exception as e:
            print(f"[WARN] Dealer assignment error for {id_pedido}: {e}")

    def notificar_cliente(self, id_pedido: str):
        print(f"[EVENT] Customer notified: order {id_pedido} ready for pickup")
