from fastapi import APIRouter
from domain.models import Client
from service.client_service import client_service

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/registro", status_code=201)
async def registro_cliente(client: Client):
    res = client_service.register_client(client)
    return {
        "mensaje": "Registro exitoso. Bienvenido a DomiLocal.",
        "data": {
            "id_cliente": res.id_cliente,
            "nombre": res.nombre,
            "rol": res.rol
        },
        "success": True
    }
