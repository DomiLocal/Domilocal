import sys
import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

# ── Path setup (must be first) ───────────────────────────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.v1.product_router import router as product_router
from api.order_api import router as order_router
from api.comercio_router import router as merchant_router

# ── Logger ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("domilocal.vendedor")

# ── App start time (for uptime) ───────────────────────────────
_start_time = datetime.now(timezone.utc)

# ── Lifespan (startup / shutdown hooks) ──────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 DomiLocal Vendedor API starting up...")
    yield
    logger.info("🛑 DomiLocal Vendedor API shutting down...")

# ── OpenAPI tag metadata ──────────────────────────────────────
tags_metadata = [
    {
        "name": "Root",
        "description": "Health checks and API information.",
    },
    {
        "name": "Merchant Management",
        "description": "Register and manage merchant (business) accounts.",
    },
    {
        "name": "Vendor Catalog",
        "description": (
            "Manage the vendor's product catalog. "
            "Supports creating, updating, and deleting products."
        ),
    },
    {
        "name": "Vendedor Orders",
        "description": (
            "Manage order status transitions. "
            "Mark orders as **ready_for_pickup** once they are prepared."
        ),
    },
]

# ── FastAPI application ───────────────────────────────────────
app = FastAPI(
    title="DomiLocal Vendedor API",
    description=(
        "## DomiLocal — Vendor Module"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request logging middleware ────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("← %s %s [%d]", request.method, request.url.path, response.status_code)
    return response

# ── Register routers ──────────────────────────────────────────
app.include_router(merchant_router)   # POST /api/v1/merchants
app.include_router(product_router)    # POST/PUT/DELETE /api/v1/merchants/{id}/products
app.include_router(order_router)      # PATCH /api/v1/orders/{id}/ready-for-pickup

# ── Root endpoint ─────────────────────────────────────────────
@app.get("/", tags=["Root"], summary="API information")
def root():
    """Returns basic API information and links to documentation."""
    return {
        "service": "DomiLocal Vendedor API",
        "version": "1.0.0",
        "status": "running",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc",
        "endpoints": {
            "merchants": "POST   /api/v1/merchants",
            "products":  "POST/PUT/DELETE /api/v1/merchants/{merchant_id}/products",
            "orders":    "PATCH  /api/v1/orders/{order_id}/ready-for-pickup",
            "health":    "GET    /health",
        },
    }

# ── Health check ──────────────────────────────────────────────
@app.get("/health", tags=["Root"], summary="Health check")
def health():
    """Returns the current health status and uptime of the service."""
    uptime_seconds = (datetime.now(timezone.utc) - _start_time).total_seconds()
    return {
        "status": "ok",
        "uptime_seconds": round(uptime_seconds, 1),
        "started_at": _start_time.isoformat(),
        "version": "1.0.0",
    }

# ── Global 404 handler ────────────────────────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Route '{request.url.path}' not found.",
            "data": None,
            "success": False,
        },
    )

# ── Global 500 handler ────────────────────────────────────────
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected internal error occurred.",
            "data": None,
            "success": False,
        },
    )

# ── Run directly with: python main.py ────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
