# ─────────────────────────────────────
# API LAYER
# Catalog endpoints
# ─────────────────────────────────────

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status
)

from service.catalog_service import (
    CatalogService
)

from repository.catalog_repository import (
    CatalogRepository
)


router = APIRouter(
    prefix="/api/v1/merchants",
    tags=["Product Catalog"]
)


repository = CatalogRepository()

service = CatalogService(
    repository
)


@router.get(
    "/{merchant_id}/products",
    status_code=status.HTTP_200_OK
)
def get_catalog(
    merchant_id: str,
    category: str | None = Query(
        default=None
    ),
    search: str | None = Query(
        default=None
    )
):

    try:

        return service.get_catalog(
            merchant_id=merchant_id,
            category=category,
            search=search
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": str(e),
                "data": None,
                "success": False
            }
        )