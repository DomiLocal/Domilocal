from fastapi import APIRouter
from typing import List, Optional
from domain.models import Vendor, Product, VendorStatus
from service.vendor_service import vendor_service
from service.order_service import order_service

router = APIRouter(prefix="/comercios", tags=["Comercios"])

@router.post("/registro", status_code=201)
async def registro_comercio(vendor: Vendor):
    res = vendor_service.register_vendor(vendor)
    return {
        "mensaje": "Comercio registrado exitosamente. Pendiente de aprobación.",
        "data": res,
        "success": True
    }

@router.get("/{id}/productos")
async def get_catalogo(id: str, categoria: Optional[str] = None):
    productos = vendor_service.get_catalog(id)
    if categoria:
        productos = [p for p in productos if p.categoria == categoria]
    return {
        "mensaje": "Catálogo obtenido exitosamente.",
        "data": {
            "id_comercio": id,
            "productos": productos
        },
        "success": True
    }

@router.post("/{id}/productos", status_code=201)
async def add_producto(id: str, product: Product):
    res = vendor_service.add_product(id, product)
    return {
        "mensaje": "Producto agregado exitosamente al catálogo.",
        "data": res,
        "success": True
    }

@router.put("/{id}/productos/{id_producto}")
async def update_producto(id: str, id_producto: str, product: Product):
    res = vendor_service.update_product(id, id_producto, product.dict(exclude_unset=True))
    return {
        "mensaje": "Producto actualizado exitosamente.",
        "data": res,
        "success": True
    }

@router.delete("/{id}/productos/{id_producto}")
async def delete_producto(id: str, id_producto: str):
    vendor_service.delete_product(id, id_producto)
    return {
        "mensaje": "Producto eliminado exitosamente.",
        "success": True
    }

@router.get("/{id}/pedidos")
async def get_pedidos(id: str, estado: Optional[OrderStatus] = None):
    res = order_service.get_vendor_orders(id, estado)
    return {
        "mensaje": "Pedidos obtenidos exitosamente.",
        "data": {
            "id_comercio": id,
            "total_pedidos": len(res),
            "pedidos": res
        },
        "success": True
    }

@router.patch("/{id}/estado")
async def update_estado(id: str, estado: VendorStatus):
    res = vendor_service.update_vendor_status(id, estado)
    return {
        "mensaje": "Estado del comercio actualizado correctamente.",
        "data": res,
        "success": True
    }
