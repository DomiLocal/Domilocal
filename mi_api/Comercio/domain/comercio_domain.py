from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class EstadoComercio(str, Enum):
    """Estados posibles del comercio"""
    PENDIENTE_APROBACION = "pendiente_aprobacion"
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    RECHAZADO = "rechazado"


class CategoriaComercio(str, Enum):
    """Categorías predefinidas de comercios"""
    RESTAURANTE = "restaurante"
    FARMACIA = "farmacia"
    TIENDA_BARRIO = "tienda_barrio"
    SUPERMERCADO = "supermercado"
    PANADERIA = "panaderia"
    CAFE = "cafe"
    HELADERIA = "heladeria"
    PIZZERIA = "pizzeria"
    PASTELERIA = "pasteleria"
    VERDULERIA = "verduleria"


class ComercioBase(BaseModel):
    """Atributos base del comercio - usados en solicitudes"""
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del negocio")
    direccion: str = Field(..., min_length=5, max_length=200, description="Dirección del comercio")
    categoria: CategoriaComercio = Field(..., description="Categoría del comercio")
    telefono: str = Field(..., min_length=7, max_length=20, description="Teléfono de contacto")
    correo: EmailStr = Field(..., description="Correo electrónico de contacto")
    
    class Config:
        use_enum_values = True


class ComercioRegistroRequest(ComercioBase):
    """Solicitud de registro de un nuevo comercio"""
    pass


class ComercioResponse(ComercioBase):
    """Respuesta con datos del comercio registrado"""
    id_comercio: str = Field(..., description="ID único del comercio")
    estado: EstadoComercio = Field(default=EstadoComercio.PENDIENTE_APROBACION)
    
    class Config:
        use_enum_values = True


class Comercio(ComercioBase):
    """Modelo de dominio completo del comercio"""
    id_comercio: str
    estado: EstadoComercio = EstadoComercio.PENDIENTE_APROBACION
    
    class Config:
        use_enum_values = True
