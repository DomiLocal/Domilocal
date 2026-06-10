from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Servidor funcionando correctamente"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development"
    }