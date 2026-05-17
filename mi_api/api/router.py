from fastapi import APIRouter
from api.client_router import router as client_router
from api.vendor_router import router as vendor_router
from api.delivery_router import router as delivery_router
from api.order_router import router as order_router

router = APIRouter(prefix="/api/v1")

router.include_router(client_router)
router.include_router(vendor_router)
router.include_router(delivery_router)
router.include_router(order_router)
