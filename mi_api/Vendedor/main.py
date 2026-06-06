<<<<<<< HEAD
import sys
import os

# Add the directory to python path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

=======
>>>>>>> Registro_negocio
# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application for Vendor
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
<<<<<<< HEAD
from api import router as product_router
from api.order_api import router as order_router
=======
from api.comercio_router import router as merchant_router
>>>>>>> Registro_negocio

# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal Vendedor API",
<<<<<<< HEAD
    description="REST API for Vendedor — Product catalog and order readiness",
=======
    description="Merchant Management API",
>>>>>>> Registro_negocio
    version="1.0.0"
)

# ── Register routers ─────────────────────────────────────────
<<<<<<< HEAD
app.include_router(product_router)
app.include_router(order_router)
=======
app.include_router(merchant_router)
>>>>>>> Registro_negocio

# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
<<<<<<< HEAD
        "message": "DomiLocal Vendedor API is running successfully 🚀",
=======
        "message": "Vendedor API is running successfully 🚀",
>>>>>>> Registro_negocio
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }

<<<<<<< HEAD
@app.get("/health", tags=["Root"])
=======
@app.get("/health")
>>>>>>> Registro_negocio
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
