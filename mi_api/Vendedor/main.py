import sys
import os

# Add the directory to python path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application for Vendor
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from api import router as product_router
from api.order_api import router as order_router

# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal Vendedor API",
    description="REST API for Vendedor — Product catalog and order readiness",
    version="1.0.0"
)

# ── Register routers ─────────────────────────────────────────
app.include_router(product_router)
app.include_router(order_router)

# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "DomiLocal Vendedor API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Root"])
def health():
    return {
        "status": "ok"
    }

# ── Run directly with: python main.py ────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
