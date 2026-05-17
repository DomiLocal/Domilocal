from typing import List, Optional
from domain.models import Vendor, Product, VendorStatus
from repository.vendor_repo import vendor_repo
from fastapi import HTTPException

class VendorService:
    def register_vendor(self, vendor: Vendor) -> Vendor:
        if vendor_repo.get_by_name_and_address(vendor.nombre, vendor.direccion):
            raise HTTPException(status_code=409, detail="Ya existe un comercio registrado con ese nombre y dirección.")
        
        vendor.estado = VendorStatus.PENDIENTE
        return vendor_repo.create(vendor)

    def get_catalog(self, vendor_id: str) -> List[Product]:
        vendor = vendor_repo.get_by_id(vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Comercio no encontrado.")
        if vendor.estado == VendorStatus.INACTIVO:
            raise HTTPException(status_code=403, detail="Este comercio no está disponible por el momento.")
            
        return [p for p in vendor.productos if p.stock > 0]

    def add_product(self, vendor_id: str, product: Product) -> Product:
        res = vendor_repo.add_product(vendor_id, product)
        if not res:
            raise HTTPException(status_code=404, detail="Comercio no encontrado.")
        return res

    def update_product(self, vendor_id: str, product_id: str, product_data: dict) -> Product:
        res = vendor_repo.update_product(vendor_id, product_id, product_data)
        if not res:
            raise HTTPException(status_code=404, detail="Producto o comercio no encontrado.")
        return res

    def delete_product(self, vendor_id: str, product_id: str) -> bool:
        if not vendor_repo.delete_product(vendor_id, product_id):
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        return True

    def update_vendor_status(self, vendor_id: str, status: VendorStatus) -> Vendor:
        res = vendor_repo.update_status(vendor_id, status)
        if not res:
            raise HTTPException(status_code=404, detail="Comercio no encontrado.")
        return res

vendor_service = VendorService()
