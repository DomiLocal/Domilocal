from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from mi_api.Vendedor.service.comercio_service import comercio_service

router = APIRouter(prefix="/api/v1/merchants")


@router.post("/{id}/confirm", tags=["Confirmation"], summary="Confirm merchant account")
def confirm_merchant(id: str):
    try:
        result = comercio_service.confirm_merchant(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except LookupError as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e), "data": None, "success": False})
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e), "data": None, "success": False})


@router.patch(
    "/{id}/status",
    tags=["Status & Availability"],
    summary="Toggle merchant status",
    description="Toggles the merchant between `active` and `inactive`. No body required. Merchant must be confirmed first.",
)
def toggle_merchant_status(id: str):
    try:
        result = comercio_service.toggle_status(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except LookupError as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e), "data": None, "success": False})
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e), "data": None, "success": False})


@router.get("/{id}", tags=["Queries"], summary="Get merchant info")
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
