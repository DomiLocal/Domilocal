# ─────────────────────────────────────
# CAPA REPOSITORIO
# Simulación BD
# ─────────────────────────────────────

from domain.comercio import Comercio


class ComercioRepository:


    def __init__(self):

        self._comercios=[]
        self._contador=1


    def obtener_por_nombre_direccion(
        self,
        nombre,
        direccion
    ):


        return next(

            (

                c for c in self._comercios

                if c.nombre.lower()==nombre.lower()
                and
                c.direccion.lower()==direccion.lower()

            ),

            None

        )


    def crear(self,datos):


        nuevo=Comercio(

            id_comercio=f"COM-{self._contador:03}",

            nombre=datos.nombre,

            direccion=datos.direccion,

            categoria=datos.categoria,

            telefono=datos.telefono,

            correo_contacto=datos.correo_contacto,

            estado="pendiente_aprobacion"

        )


        self._comercios.append(
            nuevo
        )

        self._contador+=1

        return nuevo



comercio_repository=ComercioRepository()
