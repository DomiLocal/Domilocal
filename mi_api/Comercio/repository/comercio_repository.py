from typing import Optional, List
from ..domain.comercio_domain import Comercio, EstadoComercio
import uuid


class ComercioRepository:
    """
    Capa de repositorio para gestión de datos de comercios.
    En un escenario real, esto interactuaría con una base de datos.
    """
    
    def __init__(self):
        # En memoria para propósitos de demostración
        # En producción, esto sería una conexión a base de datos
        self.comercios: dict = {}
    
    def crear_comercio(self, comercio_data: dict) -> Comercio:
        """
        Crea un nuevo comercio y lo almacena.
        
        Args:
            comercio_data: Diccionario con los datos del comercio
            
        Returns:
            Comercio: El comercio creado
        """
        id_comercio = f"COM-{str(uuid.uuid4())[:8].upper()}"
        
        comercio = Comercio(
            id_comercio=id_comercio,
            **comercio_data
        )
        
        self.comercios[id_comercio] = comercio
        return comercio
    
    def obtener_comercio_por_id(self, id_comercio: str) -> Optional[Comercio]:
        """
        Obtiene un comercio por su ID.
        
        Args:
            id_comercio: ID del comercio a buscar
            
        Returns:
            Comercio o None si no existe
        """
        return self.comercios.get(id_comercio)
    
    def existe_comercio_duplicado(self, nombre: str, direccion: str) -> bool:
        """
        Verifica si existe un comercio con el mismo nombre y dirección.
        
        Args:
            nombre: Nombre del comercio
            direccion: Dirección del comercio
            
        Returns:
            bool: True si existe duplicado, False si no
        """
        for comercio in self.comercios.values():
            if comercio.nombre.lower() == nombre.lower() and \
               comercio.direccion.lower() == direccion.lower():
                return True
        return False
    
    def obtener_comercios_por_estado(self, estado: EstadoComercio) -> List[Comercio]:
        """
        Obtiene todos los comercios por un estado específico.
        
        Args:
            estado: Estado del comercio a filtrar
            
        Returns:
            Lista de comercios con ese estado
        """
        return [
            comercio for comercio in self.comercios.values()
            if comercio.estado == estado
        ]
    
    def actualizar_estado_comercio(self, id_comercio: str, nuevo_estado: EstadoComercio) -> Optional[Comercio]:
        """
        Actualiza el estado de un comercio.
        
        Args:
            id_comercio: ID del comercio
            nuevo_estado: Nuevo estado
            
        Returns:
            Comercio actualizado o None si no existe
        """
        comercio = self.comercios.get(id_comercio)
        if comercio:
            comercio.estado = nuevo_estado
            self.comercios[id_comercio] = comercio
        return comercio
    
    def obtener_todos_comercios(self) -> List[Comercio]:
        """
        Obtiene todos los comercios registrados.
        
        Returns:
            Lista de todos los comercios
        """
        return list(self.comercios.values())
    
    def eliminar_comercio(self, id_comercio: str) -> bool:
        """
        Elimina un comercio del repositorio.
        
        Args:
            id_comercio: ID del comercio a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if id_comercio in self.comercios:
            del self.comercios[id_comercio]
            return True
        return False


# Instancia global del repositorio
comercio_repository = ComercioRepository()
