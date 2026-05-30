from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from modules
try:
    from Cliente.api.cliente_api import router as customer_router
except ImportError:
    customer_router = None

try:
    from Vendedor.api.comercio_router import router as merchant_router
except ImportError:
    merchant_router = None

try:
    from Repartidor.api.repartidor_api import router as delivery_router
except ImportError:
    delivery_router = None

# Create FastAPI application
app = FastAPI(
    title="Domilocal API",
    description="API for managing merchants, users, couriers, and customers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
if customer_router:
    app.include_router(customer_router, prefix="/api/customers", tags=["Customers"])

if merchant_router:
    app.include_router(merchant_router, prefix="/api/merchants", tags=["Merchants"])

if delivery_router:
    app.include_router(delivery_router, prefix="/api/deliveries", tags=["Deliveries"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Domilocal API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
