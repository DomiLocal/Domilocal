from fastapi import APIRouter, HTTPException, status

from mi_api.Vendedor.service.pedido_service import ServicioPedido
from mi_api.Vendedor.repository.pedido_repository import repositorio_pedido

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
# tag "Orders" intentionally kept — groups with order creation and assignment

servicio = ServicioPedido(repositorio=repositorio_pedido)


@router.patch("/{id}/ready-for-pickup")
def mark_ready_for_pickup(id: str):
    try:
        pedido = servicio.marcar_listo_para_recoger(id)
        return {
            "message": "Order marked as ready for pickup.",
            "data": {
                "order_id": pedido.id_pedido,
                "status": pedido.estado,
                "updated_at": str(pedido.fecha_actualizacion) if pedido.fecha_actualizacion else None,
            },
            "success": True,
        }
    except LookupError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
