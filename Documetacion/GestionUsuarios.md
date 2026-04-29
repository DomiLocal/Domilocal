# Historias de Usuario — DomiLocal · Cliente

**Proyecto:** DomiLocal
**Asignatura:** Servicios Web
**Institución:** Unidades Tecnológicas de Santander
**Corte:** Parcial #1
**Fecha:** Abril 2026

---

# [HU-C01] Registro en la plataforma

## Historia de Usuario

**Como** cliente,
**quiero** registrarme en la plataforma proporcionando mis datos personales,
**para que** pueda acceder a los servicios de domicilio disponibles en mi zona y realizar pedidos a comercios locales.

## Flujo Esperado

- El cliente accede al formulario de registro desde la pantalla de inicio.
- Ingresa sus datos: nombre completo, correo electrónico, contraseña, número de teléfono y dirección principal.
- El sistema valida que el correo no esté registrado previamente.
- Al completar el registro, el cliente recibe una notificación de confirmación y accede a la plataforma de forma inmediata.

## Criterios de Aceptación

### 1. Validación del formulario

- [ ] El formulario incluye los campos obligatorios: nombre completo, correo, contraseña, teléfono y dirección principal.
- [ ] El sistema valida que el correo tenga un formato válido y no esté registrado previamente.
- [ ] La contraseña debe tener mínimo 8 caracteres e incluir al menos un número.

### 2. Confirmación y acceso

- [ ] Al registrarse exitosamente, el cliente recibe una notificación de bienvenida.
- [ ] El cliente puede iniciar sesión inmediatamente tras el registro.
- [ ] El rol asignado por defecto es `cliente`.

## Notas Técnicas

### Endpoint — Registro de Cliente

| Campo | Detalle |
|---|---|
| Método HTTP | `POST` |
| Ruta | `/api/v1/clientes/registro` |

### Ejemplo de Respuesta JSON

Registro exitoso:

```json
{
  "mensaje": "Registro exitoso. Bienvenido a DomiLocal.",
  "data": {
    "id_cliente": "C-00456",
    "nombre": "Ana Gómez",
    "rol": "cliente"
  },
  "success": true
}
```

Correo ya registrado:

```json
{
  "mensaje": "El correo electrónico ya se encuentra registrado en la plataforma.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Registro exitoso

- **Precondición:** El correo no existe en el sistema.
- **Acción:** Enviar `POST` a `/api/v1/clientes/registro` con todos los campos válidos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `success` retorna `true`
  - El cliente puede iniciar sesión de forma inmediata

### Caso 2 — Correo duplicado

- **Precondición:** El correo ya está registrado en el sistema.
- **Acción:** Enviar `POST` con el mismo correo.
- **Resultado esperado:**
  - Código HTTP 409 Conflict
  - Campo `mensaje` indica el motivo del conflicto

### Caso 3 — Contraseña inválida

- **Precondición:** La contraseña no cumple los requisitos mínimos.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje`: `"La contraseña debe tener mínimo 8 caracteres e incluir al menos un número."`

### Caso 4 — Campos obligatorios faltantes

- **Acción:** Enviar `POST` omitiendo uno o más campos obligatorios.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje` describe el campo faltante

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint registra al cliente con todos sus datos y le asigna el rol `cliente`.
- [ ] Se validan duplicados de correo antes de crear la cuenta.

### Pruebas Completadas

- [ ] Se ejecutaron pruebas de validación de todos los campos obligatorios.
- [ ] Se cubrieron los casos de correo duplicado y contraseña inválida.

### Manejo de Errores

- [ ] Se retorna HTTP 400 para datos inválidos o incompletos.
- [ ] Se retorna HTTP 409 para correo duplicado.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-C02] Exploración del catálogo de productos

## Historia de Usuario

**Como** cliente,
**quiero** explorar el catálogo de productos de los comercios locales registrados en la plataforma,
**para que** pueda encontrar lo que necesito, comparar opciones y agregarlo a mi pedido fácilmente.

## Flujo Esperado

- El cliente accede a la sección de comercios disponibles en su zona.
- Selecciona un comercio y visualiza su catálogo de productos.
- Aplica filtros por categoría o busca un producto por nombre.
- Agrega el producto deseado a su pedido desde la vista del catálogo.

## Criterios de Aceptación

### 1. Visualización del catálogo

- [ ] Solo se muestran comercios activos y disponibles en la zona del cliente.
- [ ] Cada producto muestra: nombre, descripción, precio y foto (si está disponible).
- [ ] Los productos con stock igual a 0 no son visibles para el cliente.

### 2. Filtros y búsqueda

- [ ] El cliente puede filtrar productos por categoría (ej. alimentos, farmacia, mercado).
- [ ] El cliente puede buscar productos por nombre dentro de un comercio.
- [ ] El botón "Agregar al pedido" responde de forma inmediata al ser presionado.

## Notas Técnicas

### Endpoint — Catálogo de Productos por Comercio

| Campo | Detalle |
|---|---|
| Método HTTP | `GET` |
| Ruta | `/api/v1/comercios/{id}/productos` |

### Ejemplo de Respuesta JSON

Consulta exitosa:

```json
{
  "mensaje": "Catálogo obtenido exitosamente.",
  "data": {
    "id_comercio": "COM-001",
    "nombre_comercio": "Tienda La Esquina",
    "productos": [
      {
        "id_producto": "P-001",
        "nombre": "Agua 500ml",
        "descripcion": "Agua mineral sin gas",
        "precio": 1500,
        "stock": 20,
        "categoria": "bebidas",
        "foto_url": "https://domilocal.com/fotos/agua.jpg"
      }
    ]
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Catálogo con productos disponibles

- **Precondición:** El comercio tiene productos activos con stock mayor a 0.
- **Acción:** Ejecutar `GET` a `/api/v1/comercios/{id}/productos`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna la lista de productos con todos sus campos

### Caso 2 — Filtro por categoría

- **Acción:** Ejecutar `GET` con parámetro `?categoria=bebidas`.
- **Resultado esperado:**
  - Solo se retornan productos de la categoría indicada

### Caso 3 — Comercio sin productos disponibles

- **Precondición:** El comercio existe pero no tiene productos con stock mayor a 0.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Campo `data.productos` retorna una lista vacía

### Caso 4 — ID de comercio inexistente

- **Acción:** Ejecutar `GET` con un `id` de comercio que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint retorna correctamente el catálogo del comercio indicado.
- [ ] Los productos con stock igual a 0 son excluidos de la respuesta.
- [ ] El filtro por categoría y la búsqueda por nombre funcionan correctamente.

### Pruebas Completadas

- [ ] Se probaron catálogos con y sin productos disponibles.
- [ ] Se validó el filtro por categoría y la búsqueda por nombre.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el comercio no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-C03] Creación de un pedido

## Historia de Usuario

**Como** cliente,
**quiero** crear un pedido seleccionando productos de un comercio, indicando mi dirección de entrega y eligiendo mi método de pago,
**para que** reciba mis productos a domicilio sin necesidad de desplazarme.

## Flujo Esperado

- El cliente agrega productos de un comercio a su carrito.
- Revisa el resumen del pedido con productos, cantidades, subtotal, costo de envío y total.
- Ingresa o confirma su dirección de entrega.
- Selecciona el método de pago.
- Confirma el pedido y recibe una notificación con el número de confirmación generado.

## Criterios de Aceptación

### 1. Carrito y resumen

- [ ] El cliente solo puede agregar productos de un único comercio por pedido.
- [ ] El resumen del pedido muestra: productos, cantidades, subtotal, costo de envío y total.
- [ ] No es posible confirmar un pedido con el carrito vacío.

### 2. Dirección y método de pago

- [ ] El cliente puede ingresar una dirección de entrega diferente a la registrada en su perfil.
- [ ] Los métodos de pago disponibles son seleccionables (ej. efectivo al recibir, pago en línea).
- [ ] Al confirmar el pedido, el cliente recibe una notificación con el número de pedido generado.

## Notas Técnicas

### Endpoint — Creación de Pedido

| Campo | Detalle |
|---|---|
| Método HTTP | `POST` |
| Ruta | `/api/v1/pedidos` |

### Ejemplo de Respuesta JSON

Pedido creado exitosamente:

```json
{
  "mensaje": "Pedido creado exitosamente.",
  "data": {
    "id_pedido": "PED-0789",
    "estado": "recibido",
    "total": 18500,
    "metodo_pago": "efectivo",
    "direccion_entrega": "Carrera 10 #45-20, Apto 301"
  },
  "success": true
}
```

Carrito vacío:

```json
{
  "mensaje": "No es posible crear un pedido con el carrito vacío.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Pedido creado exitosamente

- **Precondición:** El cliente tiene productos en el carrito y una dirección de entrega válida.
- **Acción:** Enviar `POST` a `/api/v1/pedidos` con todos los campos requeridos.
- **Resultado esperado:**
  - Código HTTP 201 Created
  - Campo `estado`: `recibido`
  - El cliente recibe notificación con el número de pedido

### Caso 2 — Carrito vacío

- **Precondición:** El cliente intenta confirmar sin productos en el carrito.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `success` retorna `false`

### Caso 3 — Productos de múltiples comercios

- **Precondición:** El cliente intenta agregar productos de dos comercios distintos.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje`: `"Solo puedes pedir productos de un mismo comercio por pedido."`

### Caso 4 — Dirección de entrega faltante

- **Precondición:** No se especifica una dirección de entrega en la solicitud.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `mensaje` indica el campo faltante

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint crea el pedido y lo registra con estado `recibido`.
- [ ] Se valida que el carrito no esté vacío y que los productos sean de un único comercio.

### Pruebas Completadas

- [ ] Se probó la creación exitosa y los casos de validación de carrito y dirección.
- [ ] Se cubrió el intento de mezclar productos de diferentes comercios.

### Manejo de Errores

- [ ] Se retorna HTTP 400 para validaciones de negocio fallidas.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-C04] Seguimiento del pedido en tiempo real

## Historia de Usuario

**Como** cliente,
**quiero** consultar el estado actual de mi pedido en tiempo real,
**para que** pueda saber exactamente en qué etapa se encuentra la entrega y estimar cuándo llegará, sin necesidad de contactar al comercio o al repartidor.

## Flujo Esperado

- El cliente accede a la sección "Mis pedidos" en su perfil.
- Selecciona un pedido activo y visualiza su estado actual.
- El estado se actualiza automáticamente conforme avanza el proceso de entrega.
- El cliente recibe una notificación por cada cambio de estado.

## Criterios de Aceptación

### 1. Estados del pedido

- [ ] Los estados posibles del pedido son: `Recibido`, `En preparación`, `En camino`, `Entregado`.
- [ ] El estado se actualiza de forma automática, sin necesidad de recargar la pantalla.
- [ ] Cada cambio de estado genera una notificación para el cliente.

### 2. Información del repartidor e historial

- [ ] Cuando el pedido está en estado `En camino`, se muestra el nombre del repartidor asignado.
- [ ] El historial de pedidos anteriores es accesible desde la sección "Mis pedidos".

## Notas Técnicas

### Endpoint — Estado del Pedido

| Campo | Detalle |
|---|---|
| Método HTTP | `GET` |
| Ruta | `/api/v1/pedidos/{id}/estado` |

### Ejemplo de Respuesta JSON

Consulta exitosa:

```json
{
  "mensaje": "Estado del pedido obtenido exitosamente.",
  "data": {
    "id_pedido": "PED-0789",
    "estado": "en_camino",
    "repartidor": {
      "nombre": "Carlos Pérez",
      "telefono": "3009876543"
    },
    "historial_estados": [
      { "estado": "recibido", "hora": "2025-03-15T13:00:00Z" },
      { "estado": "en_preparacion", "hora": "2025-03-15T13:10:00Z" },
      { "estado": "en_camino", "hora": "2025-03-15T13:25:00Z" }
    ]
  },
  "success": true
}
```

## Casos de Prueba Funcional

### Caso 1 — Consulta de pedido en camino

- **Precondición:** El pedido existe y está en estado `En camino`.
- **Acción:** Ejecutar `GET` a `/api/v1/pedidos/{id}/estado`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Se retorna el estado actual y los datos del repartidor asignado

### Caso 2 — Historial de estados

- **Precondición:** El pedido ha transitado por múltiples estados.
- **Resultado esperado:**
  - El campo `historial_estados` contiene cada estado con su respectiva marca de tiempo

### Caso 3 — ID de pedido inexistente

- **Acción:** Ejecutar `GET` con un `id` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint retorna el estado actual y el historial completo de estados del pedido.
- [ ] Los datos del repartidor se incluyen en la respuesta cuando el pedido está en estado `En camino`.

### Pruebas Completadas

- [ ] Se probaron todos los estados posibles del pedido.
- [ ] Se validó el historial de estados con sus marcas de tiempo.

### Manejo de Errores

- [ ] Se retorna HTTP 404 si el pedido no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.

---

# [HU-C05] Cancelación de un pedido

## Historia de Usuario

**Como** cliente,
**quiero** cancelar un pedido que aún no ha sido despachado,
**para que** no se realice una entrega innecesaria cuando surja algún inconveniente o cambio de decisión de mi parte.

## Flujo Esperado

- El cliente accede al detalle de un pedido en estado `Recibido` o `En preparación`.
- Selecciona la opción "Cancelar pedido" e ingresa opcionalmente una razón.
- El sistema procesa la cancelación y notifica al comercio y al repartidor si ya fue asignado.
- El cliente recibe confirmación de que la cancelación fue procesada exitosamente.

## Criterios de Aceptación

### 1. Restricción de cancelación

- [ ] El cliente solo puede cancelar un pedido en estado `Recibido` o `En preparación`.
- [ ] Si el pedido está en estado `En camino` o `Entregado`, la opción de cancelación está deshabilitada.
- [ ] El sistema solicita opcionalmente una razón de cancelación antes de proceder.

### 2. Notificaciones tras la cancelación

- [ ] El comercio recibe una notificación inmediata de la cancelación.
- [ ] Si ya había un repartidor asignado, este también recibe la notificación y vuelve al estado `Disponible`.
- [ ] El cliente recibe confirmación de que la cancelación fue procesada exitosamente.

## Notas Técnicas

### Endpoint — Cancelación de Pedido

| Campo | Detalle |
|---|---|
| Método HTTP | `PATCH` |
| Ruta | `/api/v1/pedidos/{id}/cancelar` |

### Ejemplo de Respuesta JSON

Cancelación exitosa:

```json
{
  "mensaje": "Pedido cancelado exitosamente.",
  "data": {
    "id_pedido": "PED-0789",
    "estado": "cancelado",
    "razon": "Cambié de opinión"
  },
  "success": true
}
```

Pedido ya despachado:

```json
{
  "mensaje": "No es posible cancelar el pedido. El repartidor ya está en camino.",
  "data": null,
  "success": false
}
```

## Casos de Prueba Funcional

### Caso 1 — Cancelación exitosa en estado Recibido

- **Precondición:** El pedido está en estado `Recibido`.
- **Acción:** Ejecutar `PATCH` a `/api/v1/pedidos/{id}/cancelar`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - Estado del pedido cambia a `cancelado`
  - El comercio recibe notificación de la cancelación

### Caso 2 — Cancelación exitosa en estado En preparación

- **Precondición:** El pedido está en estado `En preparación`.
- **Resultado esperado:**
  - Código HTTP 200 OK
  - El comercio y el repartidor (si existe) reciben notificación
  - El repartidor vuelve al estado `Disponible`

### Caso 3 — Intento de cancelar pedido en camino

- **Precondición:** El pedido está en estado `En camino`.
- **Resultado esperado:**
  - Código HTTP 400 Bad Request
  - Campo `success` retorna `false`
  - Campo `mensaje` explica que el repartidor ya está en camino

### Caso 4 — ID de pedido inexistente

- **Acción:** Ejecutar `PATCH` con un `id` que no existe.
- **Resultado esperado:**
  - Código HTTP 404 Not Found

## Definición de Hecho

### Alcance Funcional

- [ ] El endpoint cancela el pedido únicamente en los estados `Recibido` y `En preparación`.
- [ ] El repartidor asignado (si existe) es notificado y vuelve al estado `Disponible`.

### Pruebas Completadas

- [ ] Se probó la cancelación exitosa en los dos estados permitidos.
- [ ] Se cubrió el intento de cancelar un pedido en estado `En camino`.

### Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos de entrada, salida y ejemplos de respuesta exitosa y de error.

### Manejo de Errores

- [ ] Se retorna HTTP 400 si el pedido no está en un estado cancelable.
- [ ] Se retorna HTTP 404 si el pedido no existe.
- [ ] Se retorna HTTP 503 si la base de datos no está disponible.
