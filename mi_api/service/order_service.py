from typing import List, Optional
from domain.models import Order, OrderStatus, DeliveryStatus
from repository.order_repo import order_repo
from repository.vendor_repo import vendor_repo
from repository.delivery_repo import delivery_repo
from fastapi import HTTPException

class OrderService:
    def create_order(self, order: Order) -> Order:
        if not order.productos:
            raise HTTPException(status_code=400, detail="No es posible crear un pedido con el carrito vacío.")
        
        # Validate all products are from the same vendor
        vendor = vendor_repo.get_by_id(order.id_comercio)
        if not vendor:
            raise HTTPException(status_code=404, detail="Comercio no encontrado.")
            
        return order_repo.create(order)

    def get_order_status(self, order_id: str) -> Order:
        order = order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        return order

    def cancel_order(self, order_id: str, reason: Optional[str] = None) -> Order:
        order = order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
            
        if order.estado not in [OrderStatus.RECIBIDO, OrderStatus.EN_PREPARACION]:
            raise HTTPException(status_code=400, detail="No es posible cancelar el pedido. El repartidor ya está en camino.")
            
        order.notas = f"{order.notas or ''} | Cancelación: {reason or 'Sin razón'}"
        return order_repo.update_status(order_id, OrderStatus.CANCELADO)

    def mark_ready(self, order_id: str) -> Order:
        order = order_repo.get_by_id(order_id)
        if not order or order.estado != OrderStatus.EN_PREPARACION:
            raise HTTPException(status_code=400, detail="El pedido no se encuentra en preparación.")
        
        updated_order = order_repo.update_status(order_id, OrderStatus.LISTO_PARA_RECOGER)
        # Auto assign logic
        self.assign_repartidor(order_id)
        return updated_order

    def assign_repartidor(self, order_id: str) -> Order:
        order = order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
            
        repartidor = delivery_repo.get_available_nearest()
        if not repartidor:
            # In a real app, this would be a background task or event
            return order
            
        order.id_repartidor = repartidor.id_repartidor
        order_repo.update_status(order_id, OrderStatus.EN_CAMINO)
        return order

    def confirm_delivery(self, order_id: str) -> Order:
        order = order_repo.get_by_id(order_id)
        if not order or order.estado != OrderStatus.EN_CAMINO:
            raise HTTPException(status_code=400, detail="El pedido no se encuentra en camino.")
            
        # Update delivery person back to available
        if order.id_repartidor:
            delivery_repo.update_availability(order.id_repartidor, DeliveryStatus.DISPONIBLE)
            
        return order_repo.update_status(order_id, OrderStatus.ENTREGADO)

    def get_vendor_orders(self, vendor_id: str, status: Optional[OrderStatus] = None) -> List[Order]:
        return order_repo.get_by_vendor(vendor_id, status)

    def get_delivery_active_order(self, dp_id: str) -> Order:
        order = order_repo.get_active_by_delivery(dp_id)
        if not order:
            raise HTTPException(status_code=404, detail="No tienes un pedido activo en este momento.")
        return order

order_service = OrderService()
