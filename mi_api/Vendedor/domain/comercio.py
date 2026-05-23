# ─────────────────────────────────────
# CAPA DOMINIO
# Reglas y modelos
# ─────────────────────────────────────

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


CATEGORIAS_VALIDAS=[

    "restaurante",
    "farmacia",
    "tienda de barrio",
    "supermercado",
    "panaderia",
    "cafeteria"

]


class ComercioCreate(BaseModel):


    nombre:str=Field(
        ...,
        min_length=3
    )

    direccion:str=Field(
        ...,
        min_length=5
    )

    categoria:str

    telefono:str=Field(
        ...,
        min_length=10
    )

    correo_contacto:EmailStr


    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls,v):

        if v.lower() not in CATEGORIAS_VALIDAS:

            raise ValueError(
                "La categoría indicada no es válida."
            )

        return v.lower()


class ComercioResponse(BaseModel):

    id_comercio:str
    nombre:str
    estado:str


class RegistroComercioResponse(BaseModel):

    mensaje:str
    data:ComercioResponse|None
    success:bool


class Comercio:


    def __init__(
        self,
        id_comercio,
        nombre,
        direccion,
        categoria,
        telefono,
        correo_contacto,
        estado="pendiente_aprobacion"
    ):


        self.id_comercio=id_comercio
        self.nombre=nombre
        self.direccion=direccion
        self.categoria=categoria
        self.telefono=telefono
        self.correo_contacto=correo_contacto
        self.estado=estado


    def visible_clientes(self):

        return self.estado=="activo"


    def to_response(self):

        return {

            "id_comercio":self.id_comercio,
            "nombre":self.nombre,
            "estado":self.estado

        }
