# ─────────────────────────────────────
# CAPA SERVICIO
# Lógica del negocio
# ─────────────────────────────────────

from domain.comercio import (

    ComercioCreate,
    ComercioResponse,
    RegistroComercioResponse

)

from repository.comercio_repository import (
    ComercioRepository
)


class ComercioService:


    def __init__(
        self,
        repo:ComercioRepository
    ):

        self.repo=repo


    def registrar(
        self,
        datos:ComercioCreate
    ):


        existe=self.repo.obtener_por_nombre_direccion(

            datos.nombre,
            datos.direccion

        )


        if existe:

            raise ValueError(
                "Ya existe un comercio registrado con ese nombre y dirección."
            )


        nuevo=self.repo.crear(
            datos
        )


        return RegistroComercioResponse(

            mensaje="Comercio registrado exitosamente. Pendiente de aprobación.",

            data=ComercioResponse(
                **nuevo.to_response()
            ),

            success=True

        )