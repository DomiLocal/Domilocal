# ─────────────────────────────────────────────────────────────
# ENTRY POINT — FastAPI application
# Registers routers and starts the server
# ─────────────────────────────────────────────────────────────

from fastapi import FastAPI

from api.client_api import router as client_router


# ── FastAPI application ──────────────────────────────────────
app = FastAPI(
    title="DomiLocal API",
    description="REST API with layered architecture using FastAPI",
    version="1.0.0"
)


# ── Register routers ─────────────────────────────────────────
app.include_router(client_router)


# ── Root endpoint ────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():

    return {
        "message": "DomiLocal API is running successfully 🚀",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }


# ── Run directly with: python main.py ───────────────────────
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )