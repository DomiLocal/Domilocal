from fastapi import APIRouter, HTTPException, status
from domain.product_domain import ProductCreate
from service.product_service import ProductService
from repository.product_repository import ProductRepository

router = APIRouter(
    prefix="/api/v1/comercios/{comercio_id}/productos",
    tags=["Catálogo de Productos"]
)

repo = ProductRepository()
service = ProductService(repo)


@router.post("", status_code=status.HTTP_201_CREATED)
def add_product(comercio_id: str, product_data: ProductCreate):
    try:
        return service.add_product(comercio_id, product_data)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(comercio_id: str, product_id: str, product_data: ProductCreate):
    try:
        return service.update_product(comercio_id, product_id, product_data)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(comercio_id: str, product_id: str):
    try:
        return service.delete_product(comercio_id, product_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
