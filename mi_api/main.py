from fastapi import FastAPI
from api.router import router as api_router

app = FastAPI(
    title="DomiLocal API",
    description="Backend para la plataforma de domicilios locales DomiLocal.",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a la API de DomiLocal",
        "docs": "/docs",
        "version": "1.0.0",
        "status": "online"
    }

# Include all routes under /api/v1
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
