from fastapi import APIRouter, HTTPException, status
from domain import ProductCreate
from service import ProductService
from repository import ProductRepository

router = APIRouter(prefix="/api/v1/merchants/{merchant_id}/products", tags=["Vendor Catalog"])

repo = ProductRepository()
service = ProductService(repo)

@router.post("", status_code=status.HTTP_201_CREATED)
def add_product(merchant_id: str, product_data: ProductCreate):
    try:
        return service.add_product(product_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(merchant_id: str, product_id: str, product_data: ProductCreate):
    try:
        return service.update_product(merchant_id, product_id, product_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(merchant_id: str, product_id: str):
    try:
        return service.delete_product(merchant_id, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))