from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class EstadoPedido(str, Enum):
    RECIBIDO = "received"
    EN_PREPARACION = "in_preparation"
    LISTO_PARA_RECOGER = "ready_for_pickup"


class PedidoRespuesta(BaseModel):
    id_pedido: str
    estado: str
    fecha_actualizacion: datetime | None = None


class Pedido:

    def __init__(
        self,
        id_pedido: str,
        estado: EstadoPedido,
        fecha_actualizacion: datetime | None = None
    ):
        self.id_pedido = id_pedido
        self.estado = estado
        self.fecha_actualizacion = fecha_actualizacion

    def marcar_listo_para_recoger(self):

        if self.estado != EstadoPedido.EN_PREPARACION:
            raise ValueError(
                "Unable to update status. The order is not in preparation."
            )

        self.estado = EstadoPedido.LISTO_PARA_RECOGER
        self.fecha_actualizacion = datetime.utcnow()

    def a_respuesta(self):
        return {
            "id_pedido": self.id_pedido,
            "estado": self.estado,
            "fecha_actualizacion": self.fecha_actualizacion
        }
