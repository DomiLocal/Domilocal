from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.comercio_api import router as comercio_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="DomiLocal - Gestión de Comercios",
    description="API REST para la gestión de comercios en la plataforma DomiLocal",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de comercios
app.include_router(comercio_router)


@app.get("/", tags=["Root"])
async def read_root():
    """Endpoint raíz de la API"""
    return {
        "mensaje": "Bienvenido a la API de Comercios de DomiLocal",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints_disponibles": {
            "registro": "POST /api/v1/comercios/registro",
            "obtener": "GET /api/v1/comercios/{id_comercio}",
            "listar_activos": "GET /api/v1/comercios",
            "pendientes_admin": "GET /api/v1/comercios/admin/pendientes",
            "aprobar": "PUT /api/v1/comercios/{id_comercio}/aprobar",
            "rechazar": "PUT /api/v1/comercios/{id_comercio}/rechazar"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "ok",
        "service": "API Comercios DomiLocal"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
