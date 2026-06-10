from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal

from service.comercio_service import comercio_service

router = APIRouter(
    prefix="/api/v1/merchants",
    tags=["Merchant Status"]
)


class StatusUpdate(BaseModel):
    status: Literal["active", "inactive"]


@router.get("/{id}")
def get_merchant(id: str):
    merchant = comercio_service.get_by_id(id)
    if not merchant:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Merchant not found.", "data": None, "success": False},
        )
    if merchant["status"] == "inactive":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "This business is currently unavailable.", "data": None, "success": False},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Merchant retrieved successfully.", "data": merchant, "success": True},
    )


@router.patch("/{id}/status")
def update_merchant_status(id: str, body: StatusUpdate):
    try:
        result = comercio_service.update_status(id, body.status)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except LookupError as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e), "data": None, "success": False},
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e), "data": None, "success": False},
        )
