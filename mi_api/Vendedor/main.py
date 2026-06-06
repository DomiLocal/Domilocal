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
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Running on port 8001 to avoid conflict if client/repartidor is on 8000
        reload=True
    )
