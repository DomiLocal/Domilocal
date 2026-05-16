# Historias de Usuario — DomiLocal · Repartidor

**Proyecto:** DomiLocal
**Asignatura:** Servicios Web
**Institución:** Unidades Tecnológicas de Santander
**Corte:** Parcial #1
**Fecha:** Abril 2026

---

# [HU-R01] Registro en la plataforma

## Historia de Usuario

**Como** repartidor,
**quiero** registrarme en la plataforma proporcionando mis datos personales, tipo de vehículo y número de licencia,
**para que** el sistema valide mi perfil y pueda comenzar a recibir asignaciones de entregas de forma oficial.

## Flujo Esperado

- El repartidor accede al formulario de registro desde la pantalla de inicio.
- Ingresa sus datos personales: nombre completo, teléfono, correo electrónico y contraseña.
- Selecciona su tipo de vehículo (moto, bicicleta, carro) e ingresa su número de licencia.
- El sistema valida que el correo y el número de licencia no estén registrados previamente.
- Al completar el registro exitosamente, el repartidor queda en estado `pendiente_activacion` y recibe una notificación de confirmación.

## Criterios de Aceptación

### 1. Validación del formulario

- [ ] El formulario incluye los campos obligatorios: nombre completo, teléfono, correo, contraseña, tipo de vehículo y número de licencia.
- [ ] El sistema valida que el correo electrónico tenga un formato válido.
- [ ] El sistema valida que el número de licencia no esté registrado previamente.
- [ ] La contraseña debe tener mínimo 8 caracteres e incluir al menos un número.

### 2. Estados y notificaciones

- [ ] Al registrarse exitosamente, el repartidor queda en estado `pendiente_activacion`.
- [ ] El sistema envía una notificación de confirmación al correo registrado.
- [ ] Un repartidor en estado `pendiente_activacion` no puede recibir asignaciones de pedidos.

## Notas Técnicas

### Endpoint — Registro de Repartidor

| Campo | Detalle |
|---|---|
| Método HTTP | `POST` |
| Ruta | `/api/v1/repartidores/registro` |

### Ejemplo de Respuesta JSON

Registro exitoso:

```json
{
  "message": "Registro exitoso. Tu cuenta está pendiente de activación.",
  "data": {
    "id_repartidor": "R-00123",
    "name": "Carlos Pérez",
    "state": "pendiente_activacion"
  },
  "success": true
}
```

Correo o licencia ya registrados:

```json
{
  "message": "El correo o número de licencia ya se encuentra registrado.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Registro exitoso

- **Precondición:** El correo y el número de licencia no existen en el sistema.
- **Acción:** Enviar `POST` a `/api/v1/repartidores/registro` con todos los campos válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - El repartidor queda con estado `pendiente_activacion`
  - Campo `success` retorna `true`
  - Se envía notificación de confirmación al correo registrado

### Caso 2 — Correo o licencia duplicados

- **Precondición:** El correo o número de licencia ya existe en la base de datos.
- **Acción:** Enviar `POST` con datos duplicados.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `message` indica el motivo del conflicto
  - Campo `success` retorna `false`

### Caso 3 — Campos obligatorios faltantes

- **Precondición:** El cuerpo de la solicitud omite uno o más campos obligatorios.
- **Acción:** Enviar `POST` con campos incompletos.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `message` describe el campo faltante

### Caso 4 — Formato de contraseña inválido

- **Precondición:** La contraseña enviada tiene menos de 8 caracteres o no incluye números.
- **Acción:** Enviar `POST` con contraseña inválida.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `message`: `"La contraseña debe tener mínimo 8 caracteres e incluir al menos un número."`

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint registra correctamente al repartidor con todos sus datos.
- [ ] Se validan duplicados de correo y número de licencia antes de crear el registro.
- [ ] El estado inicial del repartidor es `pendiente_activacion`.

### Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias de validación de campos.
- [ ] Se cubrieron los casos de error, duplicados y campos faltantes.
- [ ] Las pruebas funcionales están documentadas y aprobadas.

### Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada, salida y ejemplos de respuesta exitosa y de error.

### Manejo de Errores

- [ ] Se retorna HTTP 400 para datos inválidos o incompletos.
- [ ] Se retorna HTTP 409 para registros duplicados.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-R02] Gestión de disponibilidad

## Historia de Usuario

**Como** repartidor,
**quiero** activar o desactivar mi disponibilidad desde la plataforma,
**para que** el sistema solo me asigne pedidos cuando realmente estoy activo y en condiciones de entregar.

## Flujo Esperado

- El repartidor accede a su panel principal.
- Visualiza su estado actual de disponibilidad (`Disponible` / `No disponible`).
- Cambia su estado con una sola acción.
- El sistema actualiza el estado de forma inmediata y suspende la asignación de pedidos si el repartidor pasa a `No disponible`.

## Criterios de Aceptación

### 1. Cambio de estado

- [ ] El repartidor puede alternar entre los estados `Disponible` y `No disponible` con una sola acción.
- [ ] El cambio de estado se refleja en el sistema en menos de 5 segundos.
- [ ] El estado actual se muestra claramente en el panel del repartidor.

### 2. Restricción de asignaciones

- [ ] Mientras el repartidor está en estado `No disponible`, el sistema no le asigna ningún pedido nuevo.
- [ ] Un repartidor que cambia a `Disponible` queda habilitado de inmediato para recibir asignaciones.

## Notas Técnicas

### Endpoint — Actualización de Disponibilidad

| Campo | Detalle |
|---|---|
| Método HTTP | `PATCH` |
| Ruta | `/api/v1/repartidores/{id}/disponibilidad` |

### Ejemplo de Respuesta JSON

Actualización exitosa:

```json
{
  "message": "Estado de disponibilidad actualizado correctamente.",
  "data": {
    "id_repartidor": "R-00123",
    "availability": "disponible"
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Cambio a disponible

- **Precondición:** El repartidor está en estado `No disponible`.
- **Acción:** Ejecutar `PATCH` con `disponibilidad: "disponible"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El repartidor queda habilitado para recibir asignaciones
  - Campo `success` retorna `true`

### Caso 2 — Cambio a no disponible

- **Precondición:** El repartidor está en estado `Disponible`.
- **Acción:** Ejecutar `PATCH` con `availability: "no_disponible"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El repartidor deja de recibir nuevas asignaciones de pedidos

### Caso 3 — ID de repartidor inexistente

- **Acción:** Ejecutar `PATCH` con un `id` que no existe en el sistema.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `message`: `"Repartidor no encontrado."`

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint actualiza el estado de disponibilidad correctamente.
- [ ] El cambio impacta de inmediato la lógica de asignación de pedidos.

### Pruebas Completadas

- [ ] Se probaron los dos estados posibles y su efecto en la asignación.
- [ ] Se cubrió el caso de ID de repartidor inexistente.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el repartidor no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-R03] Asignación automática de pedidos

## Historia de Usuario

**Como** repartidor,
**quiero** ser asignado automáticamente a un pedido cuando estoy disponible y el comercio ha confirmado que el pedido está listo,
**para que** el proceso de entrega inicie sin demoras y no tenga que revisar manualmente si hay pedidos nuevos.

## Flujo Esperado

- El comercio marca un pedido como `Listo para recoger`.
- El sistema identifica al repartidor disponible más cercano al comercio.
- El sistema asigna el pedido y notifica al repartidor de forma inmediata.
- Si el repartidor no acepta en 60 segundos, el sistema reasigna a otro repartidor disponible.

## Criterios de Aceptación

### 1. Lógica de asignación

- [ ] El sistema asigna el pedido al repartidor disponible más cercano al comercio.
- [ ] Solo los repartidores con estado `Disponible` son candidatos para la asignación.
- [ ] Si no hay repartidores disponibles, el sistema reintenta la asignación cada 30 segundos.

### 2. Notificaciones y tiempos de respuesta

- [ ] El repartidor recibe una notificación inmediata al ser asignado.
- [ ] Si el repartidor no acepta en 60 segundos, el pedido se reasigna automáticamente.
- [ ] El comercio es notificado cuando un repartidor acepta la asignación.

## Notas Técnicas

### Endpoint — Asignación de Pedido a Repartidor

| Campo | Detalle |
|---|---|
| Método HTTP | `POST` |
| Ruta | `/api/v1/pedidos/{id}/asignar-repartidor` |

### Ejemplo de Respuesta JSON

Asignación exitosa:

```json
{
  "message": "Repartidor asignado exitosamente.",
  "data": {
    "id_pedido": "PED-0456",
    "id_repartidor": "R-00123",
    "nombre_repartidor": "Carlos Pérez",
    "tiempo_limite_aceptacion_segundos": 60
  },
  "success": true
}
```

Sin repartidores disponibles:

```json
{
  "message": "No hay repartidores disponibles en este momento. Reintentando en 30 segundos.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Asignación exitosa

- **Precondición:** Existe al menos un repartidor con estado `Disponible`.
- **Acción:** El comercio marca el pedido como `Listo para recoger`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El pedido queda asignado al repartidor más cercano
  - El repartidor recibe notificación inmediata

### Caso 2 — Reasignación por tiempo de espera vencido

- **Precondición:** El repartidor asignado no acepta dentro de los 60 segundos.
- **Resultado esperado:**
  - El sistema reasigna automáticamente a otro repartidor disponible
  - El repartidor original vuelve al estado `Disponible`

### Caso 3 — Sin repartidores disponibles

- **Precondición:** No hay repartidores con estado `Disponible` en el sistema.
- **Resultado esperado:**
  - Campo `success` retorna `false`
  - El sistema reintenta la asignación cada 30 segundos

## Definición de Hecho

### Alcance Funcional

- [ ] El sistema asigna automáticamente al repartidor disponible más cercano.
- [ ] La lógica de reasignación por tiempo límite funciona correctamente.

### Pruebas Completadas

- [ ] Se probó la asignación exitosa y la reasignación por tiempo de espera vencido.
- [ ] Se cubrió el escenario sin repartidores disponibles.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el pedido no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-R04] Consulta de detalles del pedido asignado

## Historia de Usuario

**Como** repartidor,
**quiero** consultar los detalles completos del pedido que me fue asignado,
**para que** pueda llegar al lugar de recogida, identificar los productos y entregar al cliente correcto sin cometer errores.

## Flujo Esperado

- El repartidor recibe la notificación de asignación de un pedido.
- Accede a la vista de detalle del pedido desde su panel.
- El sistema muestra la información completa: comercio, dirección de recogida, datos del cliente, dirección de entrega, productos y notas especiales.
- El repartidor puede abrir la dirección de entrega en un mapa con un solo toque.

## Criterios de Aceptación

### 1. Información del pedido

- [ ] Se muestra el nombre y dirección del comercio donde recoger el pedido.
- [ ] Se muestra el nombre del cliente, dirección de entrega y teléfono de contacto.
- [ ] Se lista cada producto con nombre y cantidad.
- [ ] Las notas especiales del cliente se muestran de forma destacada cuando existen.

### 2. Navegación y acceso

- [ ] La dirección de entrega incluye un enlace que abre el mapa de navegación (Google Maps u otro).
- [ ] El repartidor puede acceder al detalle del pedido en cualquier momento mientras este esté activo.

## Notas Técnicas

### Endpoint — Detalle del Pedido Activo

| Campo | Detalle |
|---|---|
| Método HTTP | `GET` |
| Ruta | `/api/v1/repartidores/{id}/pedido-activo` |

### Ejemplo de Respuesta JSON

Consulta exitosa:

```json
{
  "message": "Detalle del pedido obtenido exitosamente.",
  "data": {
    "id_pedido": "PED-0456",
    "comercio": {
      "nombre": "Tienda La Esquina",
      "direccion": "Calle 5 #12-30, Bucaramanga"
    },
    "cliente": {
      "nombre": "Ana Gómez",
      "telefono": "3001234567",
      "direccion_entrega": "Carrera 10 #45-20, Apto 301",
      "notas": "Dejar en portería si no hay respuesta"
    },
    "productos": [
      { "nombre": "Agua 500ml", "cantidad": 2 },
      { "nombre": "Pan tajado", "cantidad": 1 }
    ]
  },
  "success": true
}
```

Sin pedido activo:

```json
{
  "message": "No tienes un pedido activo en este momento.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Consulta exitosa con pedido activo

- **Precondición:** El repartidor tiene un pedido asignado en estado activo.
- **Acción:** Ejecutar `GET` a `/api/v1/repartidores/{id}/pedido-activo`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retornan todos los campos del pedido correctamente

### Caso 2 — Sin pedido activo

- **Precondición:** El repartidor no tiene ningún pedido asignado actualmente.
- **Resultado esperado:**
  - Código HTTP 404 Not Found
  - Campo `message`: `"No tienes un pedido activo en este momento."`

### Caso 3 — ID de repartidor inexistente

- **Acción:** Ejecutar `GET` con un `id` que no existe en el sistema.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint retorna correctamente todos los datos del pedido activo del repartidor.
- [ ] Las notas especiales del cliente se incluyen en la respuesta cuando existen.

### Pruebas Completadas

- [ ] Se probó la consulta con pedido activo y sin pedido activo.
- [ ] Se validó el retorno correcto de todos los campos definidos.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el repartidor no tiene pedido activo o no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-R05] Confirmación de entrega

## Historia de Usuario

**Como** repartidor,
**quiero** marcar un pedido como entregado una vez que lo he dejado en manos del cliente,
**para que** el sistema actualice el estado del pedido, notifique al cliente y yo quede disponible para recibir una nueva asignación.

## Flujo Esperado

- El repartidor completa la entrega al cliente.
- Accede al pedido activo en su panel y selecciona "Marcar como entregado".
- El sistema registra la hora de entrega y actualiza el estado del pedido a `Entregado`.
- El sistema notifica al cliente y al comercio del cierre exitoso.
- El repartidor queda en estado `Disponible` de forma automática.

## Criterios de Aceptación

### 1. Confirmación y cambio de estado

- [ ] El repartidor puede marcar el pedido como entregado únicamente si este se encuentra en estado `En camino`.
- [ ] Al confirmar, el estado del pedido cambia a `Entregado` de forma inmediata.
- [ ] El sistema registra la hora exacta de la entrega.
- [ ] El repartidor queda automáticamente en estado `Disponible` tras confirmar la entrega.

### 2. Notificaciones

- [ ] El cliente recibe una notificación indicando que su pedido fue entregado.
- [ ] El comercio recibe notificación del cierre exitoso de la entrega.

## Notas Técnicas

### Endpoint — Confirmación de Entrega

| Campo | Detalle |
|---|---|
| Método HTTP | `PATCH` |
| Ruta | `/api/v1/pedidos/{id}/confirmar-entrega` |

### Ejemplo de Respuesta JSON

Confirmación exitosa:

```json
{
  "message": "Entrega confirmada exitosamente.",
  "data": {
    "id_pedido": "PED-0456",
    "estado": "entregado",
    "hora_entrega": "2025-03-15T14:32:00Z",
    "repartidor_estado": "disponible"
  },
  "success": true
}
```

Pedido en estado incorrecto:

```json
{
  "message": "No es posible confirmar la entrega. El pedido no se encuentra en camino.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Confirmación exitosa

- **Precondición:** El pedido está en estado `En camino`.
- **Acción:** Ejecutar `PATCH` a `/api/v1/pedidos/{id}/confirmar-entrega`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Estado del pedido cambia a `entregado`
  - Se registra la hora exacta de entrega
  - El repartidor pasa a estado `disponible`
  - Cliente y comercio reciben notificación

### Caso 2 — Pedido en estado incorrecto

- **Precondición:** El pedido está en estado `Recibido` o `En preparación`.
- **Acción:** Ejecutar `PATCH` de confirmación.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `success` retorna `false`
  - Campo `message` describe el motivo del rechazo

### Caso 3 — ID de pedido inexistente

- **Acción:** Ejecutar `PATCH` con un `id` de pedido que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint confirma la entrega y actualiza correctamente el estado del pedido y del repartidor.
- [ ] Se registra la hora exacta de la entrega.
- [ ] Las notificaciones al cliente y al comercio se disparan correctamente.

### Pruebas Completadas

- [ ] Se probó la confirmación exitosa y el cambio de estado del repartidor.
- [ ] Se cubrió el intento de confirmar en un estado de pedido incorrecto.

### Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada, salida y ejemplos de respuesta exitosa y de error.

### Manejo de Errores

- [ ] Se retorna HTTP 400 si el pedido no está en el estado requerido.
- [ ] Se retorna HTTP 404 si el pedido no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.
