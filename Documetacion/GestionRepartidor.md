# Historias de Usuario — DomiLocal

**Proyecto:** DomiLocal
**Asignatura:** Servicios Web
**Institución:** Unidades Tecnológicas de Santander
**Corte:** Parcial #1
**Fecha:** Marzo 2026

---

## Repartidor

---

### HU-R01 · Registro en la plataforma

**Como** repartidor,
**quiero** registrarme en la plataforma proporcionando mis datos personales, tipo de vehículo y número de licencia,
**para que** el sistema valide mi perfil y pueda comenzar a recibir asignaciones de entregas de forma oficial.

**Criterios de Aceptación:**

- El formulario de registro debe incluir campos obligatorios: nombre completo, teléfono, correo, tipo de vehículo (moto, bicicleta, carro) y número de licencia.
- El sistema debe validar que el número de licencia tenga el formato correcto antes de completar el registro.
- Al completar el registro exitosamente, el repartidor recibe una confirmación y queda en estado "pendiente de activación".
- No se puede registrar un mismo número de licencia dos veces en el sistema.

---

### HU-R02 · Gestión de disponibilidad

**Como** repartidor,
**quiero** activar o desactivar mi disponibilidad desde la plataforma,
**para que** el sistema solo me asigne pedidos cuando realmente estoy activo y en condiciones de entregar.

**Criterios de Aceptación:**

- El repartidor puede cambiar su estado entre "Disponible" y "No disponible" con un solo clic o acción.
- El cambio de estado se refleja en el sistema en menos de 5 segundos.
- Mientras el repartidor está en estado "No disponible", el sistema no le asigna ningún pedido nuevo.
- El estado actual de disponibilidad se muestra claramente en el panel del repartidor.

---

### HU-R03 · Asignación automática de pedidos

**Como** repartidor,
**quiero** ser asignado automáticamente a un pedido cuando estoy disponible y el comercio ha confirmado que el pedido está listo,
**para que** el proceso de entrega inicie sin demoras y yo no tenga que estar revisando manualmente si hay pedidos nuevos.

**Criterios de Aceptación:**

- El sistema asigna el pedido al repartidor disponible más cercano al comercio.
- El repartidor recibe una notificación inmediata al momento de la asignación.
- Si el repartidor no acepta la asignación en 60 segundos, el sistema la reasigna a otro repartidor disponible.
- Solo los repartidores con estado "Disponible" son candidatos para la asignación.

---

### HU-R04 · Consulta de detalles del pedido asignado

**Como** repartidor,
**quiero** consultar los detalles completos del pedido que me fue asignado,
**para que** pueda llegar al lugar de recogida, identificar los productos y entregar al cliente correcto sin cometer errores.

**Criterios de Aceptación:**

- Los detalles del pedido deben incluir: nombre del comercio, dirección de recogida, nombre del cliente, dirección de entrega y listado de productos.
- La dirección de entrega debe tener un enlace o botón que abra la navegación en un mapa (Google Maps u otro).
- El repartidor puede acceder a estos detalles en cualquier momento mientras el pedido esté activo.
- Si hay alguna nota especial del cliente (ej. apartamento, instrucciones de entrega), debe mostrarse de forma destacada.

---

### HU-R05 · Confirmación de entrega

**Como** repartidor,
**quiero** marcar un pedido como entregado una vez que lo he dejado en manos del cliente,
**para que** el sistema actualice el estado del pedido, notifique al cliente y yo quede disponible para recibir una nueva asignación.

**Criterios de Aceptación:**

- El repartidor puede marcar el pedido como entregado desde su vista del pedido activo.
- Al confirmar la entrega, el sistema cambia automáticamente el estado del repartidor a "Disponible".
- El cliente recibe una notificación de que su pedido fue entregado.
- El comercio también es notificado del cierre exitoso de la entrega.
- El sistema registra la hora exacta en que se marcó la entrega como completada.
