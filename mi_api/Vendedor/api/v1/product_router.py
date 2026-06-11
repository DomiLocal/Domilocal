from fastapi import APIRouter, HTTPException, status

from mi_api.Vendedor.domain.product_domain import ProductCreate
from mi_api.Vendedor.service.product_service import ProductService
from mi_api.Vendedor.repository.product_repository import ProductRepository

router = APIRouter(
    prefix="/api/v1/merchants/{merchant_id}/products",
    tags=["Product Management"],
)

repo = ProductRepository()
service = ProductService(repo)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Add product",
    description=(
        "Add a new product to the merchant's catalog.\n\n"
        "**Available categories** (spaces or underscores both accepted):\n"
        "- `aseo`\n"
        "- `bebidas`\n"
        "- `comidas`\n"
        "- `general` *(default)*\n"
        "- `lacteos`\n"
        "- `mascotas`\n"
        "- `panaderia`\n"
        "- `snacks`"
    ),
)
def add_product(merchant_id: str, product_data: ProductCreate):
    try:
        return service.add_product(merchant_id, product_data)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(merchant_id: str, product_id: str, product_data: ProductCreate):
    try:
        return service.update_product(merchant_id, product_id, product_data)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(merchant_id: str, product_id: str):
    try:
        return service.delete_product(merchant_id, product_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
