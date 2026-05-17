from typing import List, Optional
from domain.models import Vendor, Product, VendorStatus

class VendorRepository:
    def __init__(self):
        self._vendors: List[Vendor] = []
        self._counter = 1

    def create(self, vendor: Vendor) -> Vendor:
        vendor.id_comercio = f"COM-{self._counter:03d}"
        self._vendors.append(vendor)
        self._counter += 1
        return vendor

    def get_by_name_and_address(self, name: str, address: str) -> Optional[Vendor]:
        return next((v for v in self._vendors if v.nombre == name and v.direccion == address), None)

    def get_by_id(self, vendor_id: str) -> Optional[Vendor]:
        return next((v for v in self._vendors if v.id_comercio == vendor_id), None)

    def get_all_active(self) -> List[Vendor]:
        return [v for v in self._vendors if v.estado == VendorStatus.ACTIVO]

    def update_status(self, vendor_id: str, status: VendorStatus) -> Optional[Vendor]:
        vendor = self.get_by_id(vendor_id)
        if vendor:
            vendor.estado = status
            return vendor
        return None

    # Product management within vendor
    def add_product(self, vendor_id: str, product: Product) -> Optional[Product]:
        vendor = self.get_by_id(vendor_id)
        if vendor:
            product.id_producto = f"P-{len(vendor.productos) + 1:03d}"
            product.disponible = product.stock > 0
            vendor.productos.append(product)
            return product
        return None

    def get_product(self, vendor_id: str, product_id: str) -> Optional[Product]:
        vendor = self.get_by_id(vendor_id)
        if vendor:
            return next((p for p in vendor.productos if p.id_producto == product_id), None)
        return None

    def update_product(self, vendor_id: str, product_id: str, updated_data: dict) -> Optional[Product]:
        product = self.get_product(vendor_id, product_id)
        if product:
            for key, value in updated_data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            product.disponible = product.stock > 0
            return product
        return None

    def delete_product(self, vendor_id: str, product_id: str) -> bool:
        vendor = self.get_by_id(vendor_id)
        if vendor:
            original_len = len(vendor.productos)
            vendor.productos = [p for p in vendor.productos if p.id_producto != product_id]
            return len(vendor.productos) < original_len
        return False

vendor_repo = VendorRepository()
