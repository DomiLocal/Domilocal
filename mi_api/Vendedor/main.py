<<<<<<< HEAD
# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application for Vendor
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from api import router as product_router

# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal Vendedor API",
    description="Product Management API",
    version="1.0.0"
)

# ── Register routers ─────────────────────────────────────────
app.include_router(product_router)

# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Vendedor API is running successfully 🚀",
=======
import sys
import os

# Add the directory to python path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, status
from api.order_api import router as order_router

app = FastAPI(
    title="DomiLocal Vendedor API",
    description="REST API for Vendedor (Order readiness and delivery dispatch)",
    version="1.0.0"
)

app.include_router(order_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "DomiLocal Vendedor API is running successfully 🚀",
>>>>>>> feature/hu-c03-Estado-pedido
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }

<<<<<<< HEAD
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# ── Run directly with: python main.py ────────────────────────
=======

>>>>>>> feature/hu-c03-Estado-pedido
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
<<<<<<< HEAD
        port=8000,
=======
        port=8001,  # Running on port 8001 to avoid conflict if client/repartidor is on 8000
>>>>>>> feature/hu-c03-Estado-pedido
        reload=True
    )
