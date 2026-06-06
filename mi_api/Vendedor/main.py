# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application for Vendor
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI
from api.comercio_router import router as merchant_router

# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal Vendedor API",
    description="Merchant Management API",
    version="1.0.0"
)

# ── Register routers ─────────────────────────────────────────
app.include_router(merchant_router)

# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Vendedor API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }

@app.get("/health")
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
