from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from ..domain.comercio_domain import ComercioRegistroRequest
from ..service.comercio_service import comercio_service


router = APIRouter(
    prefix="/api/v1/comercios",
    tags=["Comercios"],
    responses={404: {"description": "No encontrado"}}
)


@router.post(
    "/registro",
    status_code=201,
    summary="Registrar nuevo comercio",
    description="Permite que un vendedor registre su negocio local en la plataforma"
)
async def registrar_comercio(comercio: ComercioRegistroRequest):
    """
    **HU-V01: Registro del negocio en la plataforma**
    
    Registra un nuevo comercio con validación de datos.
    
    Validaciones:
    - Los campos obligatorios deben estar presentes
    - No puede existir otro comercio con el mismo nombre y dirección
    - La categoría debe ser válida
    
    Respuesta exitosa (201):
    ```json
    {
        "mensaje": "Comercio registrado exitosamente. Pendiente de aprobación.",
        "data": {
            "id_comercio": "COM-ABC12345",
            "nombre": "Tienda La Esquina",
            "estado": "pendiente_aprobacion"
        },
        "success": true
    }
    ```
    
    Errores posibles:
    - 400: Datos inválidos o campos faltantes
    - 409: Comercio duplicado (mismo nombre y dirección)
    
    Args:
        comercio: Datos del comercio a registrar
    
    Returns:
        dict: Respuesta con los datos del comercio registrado
    
    Raises:
        HTTPException: En caso de error en la validación
    """
    try:
        resultado = comercio_service.registrar_comercio(comercio)
        
        status_code = resultado.get("status_code", 500)
        
        if not resultado["success"]:
            raise HTTPException(
                status_code=status_code,
                detail=resultado
            )
        
        # Retornar respuesta exitosa
        return {
            "mensaje": resultado["mensaje"],
            "data": resultado["data"],
            "success": resultado["success"]
        }
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "mensaje": "Datos inválidos o campos faltantes",
                "errores": e.errors(),
                "success": False
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "mensaje": "Error interno del servidor",
                "error": str(e),
                "success": False
            }
        )


@router.get(
    "/{id_comercio}",
    summary="Obtener comercio por ID",
    description="Obtiene los datos de un comercio específico"
)
async def obtener_comercio(id_comercio: str):
    """
    Obtiene un comercio por su ID.
    
    Args:
        id_comercio: ID del comercio
    
    Returns:
        dict: Datos del comercio
    
    Raises:
        HTTPException 404: Si el comercio no existe
    """
    resultado = comercio_service.obtener_comercio(id_comercio)
    
    if not resultado["success"]:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado
        )
    
    return resultado


@router.get(
    "",
    summary="Listar comercios activos",
    description="Obtiene todos los comercios en estado activo (visibles para clientes)"
)
async def listar_comercios_activos():
    """
    Obtiene todos los comercios activos.
    
    Returns:
        dict: Lista de comercios activos
    """
    return comercio_service.obtener_comercios_activos()


@router.get(
    "/admin/pendientes",
    summary="Listar comercios pendientes",
    description="Obtiene todos los comercios pendientes de aprobación (Admin)"
)
async def listar_comercios_pendientes():
    """
    Obtiene todos los comercios pendientes de aprobación.
    Endpoint reservado para administradores.
    
    Returns:
        dict: Lista de comercios pendientes
    """
    return comercio_service.obtener_comercios_pendientes()


@router.put(
    "/{id_comercio}/aprobar",
    summary="Aprobar comercio",
    description="Aprueba un comercio pendiente de aprobación (Admin)"
)
async def aprobar_comercio(id_comercio: str):
    """
    Aprueba un comercio y lo hace visible para los clientes.
    Endpoint reservado para administradores.
    
    Args:
        id_comercio: ID del comercio a aprobar
    
    Returns:
        dict: Datos del comercio aprobado
    
    Raises:
        HTTPException 404: Si el comercio no existe
        HTTPException 400: Si el comercio no está en estado pendiente
    """
    resultado = comercio_service.aprobar_comercio(id_comercio)
    
    if not resultado["success"]:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado
        )
    
    return resultado


@router.put(
    "/{id_comercio}/rechazar",
    summary="Rechazar comercio",
    description="Rechaza un comercio pendiente de aprobación (Admin)"
)
async def rechazar_comercio(id_comercio: str):
    """
    Rechaza un comercio.
    Endpoint reservado para administradores.
    
    Args:
        id_comercio: ID del comercio a rechazar
    
    Returns:
        dict: Datos del comercio rechazado
    
    Raises:
        HTTPException 404: Si el comercio no existe
    """
    resultado = comercio_service.rechazar_comercio(id_comercio)
    
    if not resultado["success"]:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado
        )
    
    return resultado
