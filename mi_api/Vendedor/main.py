from fastapi import FastAPI

from api.comercio_router import (
    router as comercio_router
)


app=FastAPI(

    title="DomiLocal API",

    description="API gestión comercios",

    version="1.0"

)


app.include_router(
    comercio_router
)


@app.get("/")

def root():

    return {

        "mensaje":"API funcionando 🚀"

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