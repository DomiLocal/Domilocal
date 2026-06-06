from fastapi import APIRouter, HTTPException, status
from domain.comercio import MerchantCreate
from service.comercio_service import MerchantService
from repository.comercio_repository import MerchantRepository

router = APIRouter(prefix="/api/v1/merchants", tags=["Merchant Management"])

repo = MerchantRepository()
service = MerchantService(repo)

@router.post("", status_code=status.HTTP_201_CREATED)
def register_merchant(merchant_data: MerchantCreate):
    try:
        return service.register(merchant_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
