from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DomiLocal API funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}