from typing import Optional, List
from ..domain.comercio_domain import (
    Comercio,
    ComercioRegistroRequest,
    ComercioResponse,
    EstadoComercio,
    CategoriaComercio
)
from ..repository.comercio_repository import comercio_repository


class ComercioService:
    """
    Capa de servicio para la lógica de negocio de comercios.
    Aquí se implementa toda la validación y reglas de negocio.
    """
    
    def __init__(self, repository=None):
        self.repository = repository or comercio_repository
    
    def registrar_comercio(self, comercio_data: ComercioRegistroRequest) -> dict:
        """
        Registra un nuevo comercio con todas las validaciones.
        
        Validaciones:
        - Verifica que el nombre y dirección no existan
        - Valida que la categoría sea válida
        - Valida que los campos requeridos estén presentes
        
        Args:
            comercio_data: Datos del comercio a registrar
            
        Returns:
            dict: Respuesta con el resultado del registro
        """
        # Validación: verificar duplicado por nombre y dirección
        if self.repository.existe_comercio_duplicado(
            comercio_data.nombre,
            comercio_data.direccion
        ):
            return {
                "mensaje": "Ya existe un comercio registrado con ese nombre y dirección.",
                "data": None,
                "success": False,
                "status_code": 409
            }
        
        # Validación: verificar que la categoría sea válida
        try:
            categoria_valida = CategoriaComercio(comercio_data.categoria)
        except ValueError:
            return {
                "mensaje": "La categoría indicada no es válida.",
                "data": None,
                "success": False,
                "status_code": 400
            }
        
        # Crear el comercio en el repositorio
        comercio_dict = {
            "nombre": comercio_data.nombre,
            "direccion": comercio_data.direccion,
            "categoria": comercio_data.categoria,
            "telefono": comercio_data.telefono,
            "correo": comercio_data.correo,
            "estado": EstadoComercio.PENDIENTE_APROBACION
        }
        
        comercio_creado = self.repository.crear_comercio(comercio_dict)
        
        return {
            "mensaje": "Comercio registrado exitosamente. Pendiente de aprobación.",
            "data": {
                "id_comercio": comercio_creado.id_comercio,
                "nombre": comercio_creado.nombre,
                "estado": comercio_creado.estado
            },
            "success": True,
            "status_code": 201
        }
    
    def obtener_comercio(self, id_comercio: str) -> dict:
        """
        Obtiene un comercio por su ID.
        
        Args:
            id_comercio: ID del comercio
            
        Returns:
            dict: Respuesta con los datos del comercio
        """
        comercio = self.repository.obtener_comercio_por_id(id_comercio)
        
        if not comercio:
            return {
                "mensaje": f"Comercio con ID {id_comercio} no encontrado.",
                "data": None,
                "success": False,
                "status_code": 404
            }
        
        return {
            "mensaje": "Comercio obtenido exitosamente.",
            "data": comercio.dict(),
            "success": True,
            "status_code": 200
        }
    
    def obtener_comercios_activos(self) -> dict:
        """
        Obtiene todos los comercios en estado activo (visibles para clientes).
        
        Returns:
            dict: Respuesta con la lista de comercios activos
        """
        comercios = self.repository.obtener_comercios_por_estado(
            EstadoComercio.ACTIVO
        )
        
        return {
            "mensaje": "Comercios activos obtenidos exitosamente.",
            "data": [comercio.dict() for comercio in comercios],
            "cantidad": len(comercios),
            "success": True,
            "status_code": 200
        }
    
    def obtener_comercios_pendientes(self) -> dict:
        """
        Obtiene todos los comercios pendientes de aprobación (admin).
        
        Returns:
            dict: Respuesta con la lista de comercios pendientes
        """
        comercios = self.repository.obtener_comercios_por_estado(
            EstadoComercio.PENDIENTE_APROBACION
        )
        
        return {
            "mensaje": "Comercios pendientes de aprobación obtenidos exitosamente.",
            "data": [comercio.dict() for comercio in comercios],
            "cantidad": len(comercios),
            "success": True,
            "status_code": 200
        }
    
    def aprobar_comercio(self, id_comercio: str) -> dict:
        """
        Aprueba un comercio (cambio de estado a activo).
        Solo un administrador puede hacer esto.
        
        Args:
            id_comercio: ID del comercio a aprobar
            
        Returns:
            dict: Respuesta con el resultado
        """
        comercio = self.repository.obtener_comercio_por_id(id_comercio)
        
        if not comercio:
            return {
                "mensaje": f"Comercio con ID {id_comercio} no encontrado.",
                "data": None,
                "success": False,
                "status_code": 404
            }
        
        if comercio.estado != EstadoComercio.PENDIENTE_APROBACION:
            return {
                "mensaje": f"El comercio no está en estado pendiente de aprobación. Estado actual: {comercio.estado}",
                "data": None,
                "success": False,
                "status_code": 400
            }
        
        comercio_actualizado = self.repository.actualizar_estado_comercio(
            id_comercio,
            EstadoComercio.ACTIVO
        )
        
        return {
            "mensaje": "Comercio aprobado exitosamente. Ahora es visible para los clientes.",
            "data": {
                "id_comercio": comercio_actualizado.id_comercio,
                "nombre": comercio_actualizado.nombre,
                "estado": comercio_actualizado.estado
            },
            "success": True,
            "status_code": 200
        }
    
    def rechazar_comercio(self, id_comercio: str) -> dict:
        """
        Rechaza un comercio (cambio de estado a rechazado).
        Solo un administrador puede hacer esto.
        
        Args:
            id_comercio: ID del comercio a rechazar
            
        Returns:
            dict: Respuesta con el resultado
        """
        comercio = self.repository.obtener_comercio_por_id(id_comercio)
        
        if not comercio:
            return {
                "mensaje": f"Comercio con ID {id_comercio} no encontrado.",
                "data": None,
                "success": False,
                "status_code": 404
            }
        
        comercio_actualizado = self.repository.actualizar_estado_comercio(
            id_comercio,
            EstadoComercio.RECHAZADO
        )
        
        return {
            "mensaje": "Comercio rechazado.",
            "data": {
                "id_comercio": comercio_actualizado.id_comercio,
                "nombre": comercio_actualizado.nombre,
                "estado": comercio_actualizado.estado
            },
            "success": True,
            "status_code": 200
        }


# Instancia global del servicio
comercio_service = ComercioService()
