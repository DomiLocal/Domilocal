from fastapi import APIRouter
from domain.models import DeliveryPerson, DeliveryStatus
from service.delivery_service import delivery_service

router = APIRouter(prefix="/repartidores", tags=["Repartidores"])

@router.post("/registro", status_code=201)
async def registro_repartidor(dp: DeliveryPerson):
    res = delivery_service.register_repartidor(dp)
    return {
        "mensaje": "Registro exitoso. Tu cuenta está pendiente de activación.",
        "data": {
            "id_repartidor": res.id_repartidor,
            "nombre": res.nombre,
            "estado": res.estado
        },
        "success": True
    }

@router.patch("/{id}/disponibilidad")
async def update_disponibilidad(id: str, disponibilidad: DeliveryStatus):
    res = delivery_service.update_availability(id, disponibilidad)
    return {
        "mensaje": "Estado de disponibilidad actualizado correctamente.",
        "data": res,
        "success": True
    }

@router.get("/{id}/pedido-activo")
async def get_pedido_activo(id: str):
    from service.order_service import order_service
    res = order_service.get_delivery_active_order(id)
    return {
        "mensaje": "Detalle del pedido obtenido exitosamente.",
        "data": res,
        "success": True
    }
