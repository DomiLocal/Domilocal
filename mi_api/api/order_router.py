from fastapi import APIRouter
from typing import Optional
from domain.models import Order, OrderStatus
from service.order_service import order_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", status_code=201)
async def create_pedido(order: Order):
    res = order_service.create_order(order)
    return {
        "mensaje": "Pedido creado exitosamente.",
        "data": res,
        "success": True
    }

@router.get("/{id}/estado")
async def get_estado(id: str):
    res = order_service.get_order_status(id)
    return {
        "mensaje": "Estado del pedido obtenido exitosamente.",
        "data": res,
        "success": True
    }

@router.patch("/{id}/cancelar")
async def cancelar_pedido(id: str, razon: Optional[str] = None):
    res = order_service.cancel_order(id, razon)
    return {
        "mensaje": "Pedido cancelado exitosamente.",
        "data": res,
        "success": True
    }

@router.patch("/{id}/listo-para-recoger")
async def mark_ready(id: str):
    res = order_service.mark_ready(id)
    return {
        "mensaje": "Pedido marcado como listo para recoger.",
        "data": res,
        "success": True
    }

@router.patch("/{id}/confirmar-entrega")
async def confirm_delivery(id: str):
    res = order_service.confirm_delivery(id)
    return {
        "mensaje": "Entrega confirmada exitosamente.",
        "data": res,
        "success": True
    }
