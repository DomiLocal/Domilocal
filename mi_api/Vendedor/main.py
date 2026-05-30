from fastapi import FastAPI

from api.comercio_router import (
    router as merchant_router
)


app = FastAPI(
    title="DomiLocal API",
    description="Merchant management API",
    version="1.0"
)


app.include_router(
    merchant_router
)


@app.get("/")
def root():
    return {
        "message": "API is running 🚀"
    }


@app.get("/health")

def health():

    return {

        "status":"ok"

    }


if __name__=="__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )