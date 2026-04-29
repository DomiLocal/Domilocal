# Historias de Usuario — DomiLocal · Vendedor (Comercio)

**Proyecto:** DomiLocal
**Asignatura:** Servicios Web
**Institución:** Unidades Tecnológicas de Santander
**Corte:** Parcial #1
**Fecha:** Marzo 2026

---

# [HU-V01] Registro del negocio en la plataforma

## Historia de Usuario

**Como** vendedor,
**quiero** registrar mi negocio local en la plataforma indicando nombre, dirección, categoría y datos de contacto,
**para que** los clientes puedan encontrarme dentro de DomiLocal y empezar a realizarme pedidos sin intermediarios.

## Flujo Esperado

- El vendedor accede al formulario de registro de comercios.
- Ingresa los datos del negocio: nombre, dirección, categoría, teléfono y correo de contacto.
- El sistema valida que no exista otro comercio con el mismo nombre y dirección.
- El comercio queda en estado `pendiente_aprobacion` hasta ser activado por un administrador.
- Al ser activado, el comercio es visible para los clientes en su zona.

## Criterios de Aceptación

### 1. Validación del formulario

- [ ] El formulario incluye los campos obligatorios: nombre del negocio, dirección, categoría, teléfono y correo de contacto.
- [ ] El sistema valida que no exista otro comercio registrado con el mismo nombre y dirección.
- [ ] La categoría debe seleccionarse de una lista predefinida (ej. restaurante, farmacia, tienda de barrio).

### 2. Estado y visibilidad

- [ ] Al completar el registro, el comercio queda en estado `pendiente_aprobacion`.
- [ ] El vendedor recibe una notificación de confirmación del registro.
- [ ] El comercio solo es visible para los clientes cuando su estado es `activo`.

## Notas Técnicas

### Endpoint — Registro de Comercio

| Campo | Detalle |
|---|---|
| Método HTTP | `POST` |
| Ruta | `/api/v1/comercios/registro` |

### Ejemplo de Respuesta JSON

Registro exitoso:

```json
{
  "mensaje": "Comercio registrado exitosamente. Pendiente de aprobación.",
  "data": {
    "id_comercio": "COM-001",
    "nombre": "Tienda La Esquina",
    "estado": "pendiente_aprobacion"
  },
  "success": true
}
```

Comercio ya existente:

```json
{
  "mensaje": "Ya existe un comercio registrado con ese nombre y dirección.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Registro exitoso

- **Precondición:** No existe un comercio con el mismo nombre y dirección.
- **Acción:** Enviar `POST` a `/api/v1/comercios/registro` con todos los campos válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Estado del comercio: `pendiente_aprobacion`
  - Campo `success` retorna `true`

### Caso 2 — Comercio duplicado

- **Precondición:** Ya existe un comercio con el mismo nombre y dirección en el sistema.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `success` retorna `false`

### Caso 3 — Campos obligatorios faltantes

- **Acción:** Enviar `POST` omitiendo uno o más campos obligatorios.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje` describe el campo faltante

### Caso 4 — Categoría inválida

- **Acción:** Enviar `POST` con una categoría que no existe en la lista predefinida.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje`: `"La categoría indicada no es válida."`

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint registra el comercio con estado `pendiente_aprobacion`.
- [ ] Se validan duplicados por nombre y dirección antes de crear el registro.
- [ ] La categoría se valida contra la lista predefinida del sistema.

### Pruebas Completadas

- [ ] Se probó el registro exitoso y el rechazo por duplicado.
- [ ] Se cubrieron los casos de campos faltantes y categoría inválida.

### Manejo de Errores

- [ ] Se retorna HTTP 400 para datos inválidos o incompletos.
- [ ] Se retorna HTTP 409 para comercio duplicado.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-V02] Gestión del catálogo de productos

## Historia de Usuario

**Como** vendedor,
**quiero** agregar, editar y eliminar productos de mi catálogo incluyendo nombre, precio, stock y descripción,
**para que** mi oferta siempre esté actualizada y los clientes no puedan realizar pedidos de productos no disponibles.

## Flujo Esperado

- El vendedor accede al panel de administración de su catálogo.
- Agrega un nuevo producto completando el formulario con nombre, precio, stock y descripción.
- Edita los campos de un producto existente cuando sea necesario.
- Elimina un producto previa confirmación del sistema.
- Los cambios se reflejan de inmediato en el catálogo visible para los clientes.

## Criterios de Aceptación

### 1. Agregar producto

- [ ] Los campos obligatorios son nombre y precio. Stock y descripción son opcionales (stock por defecto: 0).
- [ ] Al agregar un producto con stock igual a 0, este queda marcado automáticamente como `No disponible`.

### 2. Editar producto

- [ ] El vendedor puede editar cualquier campo de un producto existente en cualquier momento.
- [ ] Los cambios en precio y stock se reflejan de inmediato en el catálogo del cliente.

### 3. Eliminar producto

- [ ] Al eliminar un producto, el sistema solicita confirmación antes de proceder.
- [ ] Un producto eliminado desaparece del catálogo de forma inmediata.

## Notas Técnicas

### Endpoints — Gestión de Catálogo

| Acción | Método HTTP | Ruta |
|---|---|---|
| Agregar producto | `POST` | `/api/v1/comercios/{id}/productos` |
| Editar producto | `PUT` | `/api/v1/comercios/{id}/productos/{id_producto}` |
| Eliminar producto | `DELETE` | `/api/v1/comercios/{id}/productos/{id_producto}` |

### Ejemplo de Respuesta JSON — Agregar producto

Producto con stock disponible:

```json
{
  "mensaje": "Producto agregado exitosamente al catálogo.",
  "data": {
    "id_producto": "P-001",
    "nombre": "Agua 500ml",
    "precio": 1500,
    "stock": 20,
    "disponible": true
  },
  "success": true
}
```

Producto con stock en 0:

```json
{
  "mensaje": "Producto agregado. Marcado como No disponible por stock en 0.",
  "data": {
    "id_producto": "P-002",
    "nombre": "Pan tajado",
    "precio": 3200,
    "stock": 0,
    "disponible": false
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Agregar producto exitosamente

- **Precondición:** El comercio existe y está activo.
- **Acción:** Enviar `POST` con nombre, precio y stock mayor a 0.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Producto visible de inmediato en el catálogo del cliente

### Caso 2 — Agregar producto con stock en 0

- **Acción:** Enviar `POST` con `stock: 0`.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `disponible`: `false`
  - Producto no aparece en el catálogo del cliente

### Caso 3 — Edición exitosa de producto

- **Acción:** Enviar `PUT` actualizando el precio de un producto existente.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El cambio se refleja de inmediato en el catálogo

### Caso 4 — Eliminar producto inexistente

- **Acción:** Enviar `DELETE` con un `id_producto` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] Los tres endpoints (agregar, editar, eliminar) funcionan correctamente.
- [ ] Los productos con stock igual a 0 se marcan automáticamente como no disponibles.
- [ ] Los cambios en el catálogo se reflejan de inmediato para el cliente.

### Pruebas Completadas

- [ ] Se probaron los tres flujos: agregar, editar y eliminar.
- [ ] Se validó el comportamiento automático con stock en 0.

### Documentación Técnica

- [ ] Los tres endpoints están documentados en Swagger / OpenAPI.

### Manejo de Errores

- [ ] Se retorna HTTP 400 para campos obligatorios faltantes.
- [ ] Se retorna HTTP 404 si el producto o el comercio no existen.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-V03] Consulta y gestión de pedidos recibidos

## Historia de Usuario

**Como** vendedor,
**quiero** consultar todos los pedidos que han llegado a mi comercio junto con sus detalles y estado actual,
**para que** pueda gestionarlos de forma ordenada y garantizar una atención oportuna a cada cliente.

## Flujo Esperado

- El vendedor accede al panel de pedidos de su comercio.
- Visualiza la lista de pedidos con su estado, productos y datos del cliente.
- Aplica filtros por estado para gestionar la atención de forma priorizada.
- Los pedidos nuevos generan una alerta en el panel del vendedor.

## Criterios de Aceptación

### 1. Vista de pedidos

- [ ] El panel muestra todos los pedidos con: número de pedido, nombre del cliente, productos, total y estado actual.
- [ ] Los pedidos se ordenan por defecto del más reciente al más antiguo.
- [ ] Al ingresar al detalle de un pedido, se muestran los productos con cantidades y notas del cliente.

### 2. Alertas y filtros

- [ ] Los pedidos nuevos generan una alerta visual o sonora en el panel del vendedor.
- [ ] El vendedor puede filtrar pedidos por estado: `Recibido`, `En preparación`, `Listo para recoger`, `Entregado`, `Cancelado`.

## Notas Técnicas

### Endpoint — Pedidos del Comercio

| Campo | Detalle |
|---|---|
| Método HTTP | `GET` |
| Ruta | `/api/v1/comercios/{id}/pedidos` |

### Ejemplo de Respuesta JSON

Consulta exitosa:

```json
{
  "mensaje": "Pedidos obtenidos exitosamente.",
  "data": {
    "id_comercio": "COM-001",
    "total_pedidos": 3,
    "pedidos": [
      {
        "id_pedido": "PED-0789",
        "cliente": "Ana Gómez",
        "estado": "recibido",
        "total": 18500,
        "productos": [
          { "nombre": "Agua 500ml", "cantidad": 2 },
          { "nombre": "Pan tajado", "cantidad": 1 }
        ],
        "notas": "Sin sal por favor"
      }
    ]
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Consulta con pedidos activos

- **Precondición:** El comercio tiene pedidos registrados.
- **Acción:** Ejecutar `GET` a `/api/v1/comercios/{id}/pedidos`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna la lista de pedidos con todos sus campos

### Caso 2 — Filtro por estado

- **Acción:** Ejecutar `GET` con parámetro `?estado=recibido`.
- **Resultado esperado:**
  - Solo se retornan los pedidos en estado `Recibido`

### Caso 3 — Comercio sin pedidos

- **Precondición:** El comercio existe pero no tiene pedidos registrados.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data.pedidos` retorna una lista vacía

### Caso 4 — ID de comercio inexistente

- **Acción:** Ejecutar `GET` con un `id` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint retorna correctamente la lista de pedidos del comercio.
- [ ] El filtro por estado funciona correctamente para todos los valores posibles.
- [ ] Las notas del cliente se incluyen en el detalle de cada pedido.

### Pruebas Completadas

- [ ] Se probó la consulta con pedidos activos y sin pedidos.
- [ ] Se validó el filtro por estado con todos los valores definidos.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el comercio no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-V04] Actualización del estado del pedido

## Historia de Usuario

**Como** vendedor,
**quiero** actualizar el estado de un pedido a "Listo para recoger" una vez que lo haya preparado,
**para que** el sistema pueda asignar automáticamente un repartidor y el proceso de entrega continúe sin retrasos.

## Flujo Esperado

- El vendedor accede al detalle de un pedido en estado `En preparación`.
- Selecciona la opción "Marcar como listo para recoger".
- El sistema actualiza el estado del pedido y notifica al módulo de asignación de repartidores.
- El cliente recibe una notificación de que su pedido está listo.

## Criterios de Aceptación

### 1. Cambio de estado

- [ ] El vendedor solo puede marcar un pedido como `Listo para recoger` si este está en estado `En preparación`.
- [ ] El cambio de estado queda registrado con la hora exacta en que se realizó.
- [ ] No es posible revertir el pedido a un estado anterior una vez marcado como `Listo para recoger`.

### 2. Notificaciones y asignación

- [ ] Al actualizar el estado, el sistema notifica de inmediato al módulo de asignación de repartidores.
- [ ] El cliente recibe una notificación indicando que su pedido está listo.

## Notas Técnicas

### Endpoint — Actualización de Estado de Pedido

| Campo | Detalle |
|---|---|
| Método HTTP | `PATCH` |
| Ruta | `/api/v1/pedidos/{id}/listo-para-recoger` |

### Ejemplo de Respuesta JSON

Actualización exitosa:

```json
{
  "mensaje": "Pedido marcado como listo para recoger.",
  "data": {
    "id_pedido": "PED-0789",
    "estado": "listo_para_recoger",
    "hora_actualizacion": "2025-03-15T13:20:00Z"
  },
  "success": true
}
```

Estado de pedido incorrecto:

```json
{
  "mensaje": "No es posible actualizar el estado. El pedido no se encuentra en preparación.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Actualización exitosa

- **Precondición:** El pedido está en estado `En preparación`.
- **Acción:** Ejecutar `PATCH` a `/api/v1/pedidos/{id}/listo-para-recoger`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Estado cambia a `listo_para_recoger`
  - Se registra la hora exacta del cambio
  - El módulo de repartidores recibe la señal de asignación
  - El cliente recibe notificación

### Caso 2 — Estado incorrecto del pedido

- **Precondición:** El pedido está en estado `Recibido` o `Listo para recoger`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `success` retorna `false`
  - Campo `mensaje` describe el motivo del rechazo

### Caso 3 — ID de pedido inexistente

- **Acción:** Ejecutar `PATCH` con un `id` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint actualiza el estado del pedido únicamente desde el estado `En preparación`.
- [ ] Se registra la hora exacta del cambio de estado.
- [ ] El módulo de asignación de repartidores es notificado correctamente.

### Pruebas Completadas

- [ ] Se probó la actualización exitosa y el intento desde un estado incorrecto.
- [ ] Se validó la notificación al cliente y al módulo de repartidores.

### Manejo de Errores

- [ ] Se retorna HTTP 400 si el pedido no está en el estado requerido.
- [ ] Se retorna HTTP 404 si el pedido no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-V05] Desactivación temporal del comercio

## Historia de Usuario

**Como** vendedor,
**quiero** desactivar temporalmente mi comercio cuando no pueda atender pedidos,
**para que** los clientes no puedan realizarme órdenes que no seré capaz de cumplir, evitando inconvenientes y malas experiencias.

## Flujo Esperado

- El vendedor accede a la configuración de su comercio en el panel de administración.
- Cambia su estado a `Inactivo` con una sola acción.
- El comercio desaparece del catálogo visible para los clientes de forma inmediata.
- Los pedidos en curso al momento de la desactivación no se cancelan y deben ser gestionados manualmente.
- El vendedor puede reactivar su comercio en cualquier momento.

## Criterios de Aceptación

### 1. Activación y desactivación

- [ ] El vendedor puede cambiar el estado de su comercio entre `Activo` e `Inactivo` con una sola acción.
- [ ] El cambio se refleja de forma inmediata en la plataforma.
- [ ] Mientras el comercio está `Inactivo`, no aparece en el catálogo de comercios disponibles para los clientes.

### 2. Pedidos en curso y acceso directo

- [ ] Los pedidos que ya estaban activos al momento de la desactivación no se cancelan automáticamente.
- [ ] Si un cliente accede al comercio mediante un enlace directo mientras está inactivo, el sistema muestra el mensaje: `"Este comercio no está disponible por el momento."`.

## Notas Técnicas

### Endpoint — Cambio de Estado del Comercio

| Campo | Detalle |
|---|---|
| Método HTTP | `PATCH` |
| Ruta | `/api/v1/comercios/{id}/estado` |

### Ejemplo de Respuesta JSON

Desactivación exitosa:

```json
{
  "mensaje": "Estado del comercio actualizado correctamente.",
  "data": {
    "id_comercio": "COM-001",
    "nombre": "Tienda La Esquina",
    "estado": "inactivo"
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Desactivación exitosa

- **Precondición:** El comercio está en estado `Activo`.
- **Acción:** Ejecutar `PATCH` con `estado: "inactivo"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El comercio desaparece del catálogo de clientes de forma inmediata

### Caso 2 — Reactivación exitosa

- **Precondición:** El comercio está en estado `Inactivo`.
- **Acción:** Ejecutar `PATCH` con `estado: "activo"`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El comercio vuelve a ser visible para los clientes de inmediato

### Caso 3 — Acceso directo a comercio inactivo

- **Precondición:** El comercio está en estado `Inactivo`.
- **Acción:** Un cliente intenta acceder al comercio mediante un enlace directo.
- **Resultado esperado:**
  - Se muestra el mensaje: `"Este comercio no está disponible por el momento."`

### Caso 4 — ID de comercio inexistente

- **Acción:** Ejecutar `PATCH` con un `id` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint actualiza el estado del comercio entre `activo` e `inactivo`.
- [ ] El cambio impacta de inmediato la visibilidad del comercio para los clientes.
- [ ] Los pedidos en curso no se cancelan automáticamente al desactivar el comercio.

### Pruebas Completadas

- [ ] Se probó la desactivación y reactivación del comercio.
- [ ] Se validó que los pedidos activos no se cancelen de forma automática.
- [ ] Se cubrió el acceso directo de un cliente a un comercio inactivo.

### Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada, salida y ejemplos de respuesta exitosa y de error.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el comercio no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.
