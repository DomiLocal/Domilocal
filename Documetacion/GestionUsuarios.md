# Historias de Usuario — DomiLocal

**Proyecto:** DomiLocal
**Asignatura:** Servicios Web
**Institución:** Unidades Tecnológicas de Santander
**Corte:** Parcial #1
**Fecha:** Marzo 2026

---

## Usuario (Cliente)

---

### HU-C01 · Registro en la plataforma

**Como** cliente,
**quiero** registrarme en la plataforma proporcionando mis datos personales,
**para que** pueda acceder a los servicios de domicilio disponibles en mi zona y realizar pedidos a comercios locales.

**Criterios de Aceptación:**

- El formulario de registro debe incluir campos obligatorios: nombre completo, correo electrónico, contraseña, número de teléfono y dirección principal.
- El sistema debe validar que el correo no esté registrado previamente antes de crear la cuenta.
- Al completar el registro, el cliente recibe un correo o mensaje de confirmación.
- La contraseña debe tener mínimo 8 caracteres e incluir al menos un número.
- El cliente queda con el rol "Cliente" por defecto al finalizar el registro.

---

### HU-C02 · Exploración del catálogo de productos

**Como** cliente,
**quiero** explorar el catálogo de productos de los comercios locales registrados en la plataforma,
**para que** pueda encontrar lo que necesito, comparar opciones y agregarlo a mi pedido fácilmente.

**Criterios de Aceptación:**

- El catálogo muestra únicamente comercios activos y disponibles en la zona del cliente.
- Cada producto debe mostrar: nombre, descripción, precio y foto (si está disponible).
- El cliente puede filtrar productos por categoría (ej. alimentos, farmacia, mercado).
- El cliente puede buscar productos por nombre dentro de un comercio.
- El botón "Agregar al pedido" es visible en cada producto y responde de forma inmediata.

---

### HU-C03 · Creación de un pedido

**Como** cliente,
**quiero** crear un pedido seleccionando productos de un comercio, indicando mi dirección de entrega y eligiendo mi método de pago,
**para que** reciba mis productos a domicilio de forma rápida y sin necesidad de desplazarme.

**Criterios de Aceptación:**

- El cliente solo puede agregar productos de un único comercio por pedido.
- Antes de confirmar, el sistema muestra un resumen del pedido con productos, cantidades, subtotal, costo de envío y total.
- El cliente puede ingresar una dirección de entrega diferente a la registrada en su perfil.
- Los métodos de pago disponibles deben ser seleccionables (ej. efectivo al recibir, pago en línea).
- Al confirmar el pedido, el cliente recibe una notificación con el número de pedido generado.
- No es posible confirmar un pedido si el carrito está vacío.

---

### HU-C04 · Seguimiento del pedido en tiempo real

**Como** cliente,
**quiero** consultar el estado actual de mi pedido en tiempo real,
**para que** pueda saber exactamente en qué etapa se encuentra la entrega y estimar cuándo llegará, sin necesidad de contactar al comercio o al repartidor.

**Criterios de Aceptación:**

- El estado del pedido debe actualizarse automáticamente entre las siguientes etapas: *Recibido → En preparación → En camino → Entregado*.
- El cliente puede ver el estado desde la sección "Mis pedidos" en su perfil.
- Cada cambio de estado genera una notificación para el cliente.
- Cuando el pedido está "En camino", se muestra el nombre del repartidor asignado.
- El historial de pedidos anteriores también es accesible desde la misma sección.

---

### HU-C05 · Cancelación de un pedido

**Como** cliente,
**quiero** cancelar un pedido que aún no ha sido despachado,
**para que** no se realice una entrega innecesaria cuando surja algún inconveniente o cambio de decisión de mi parte.

**Criterios de Aceptación:**

- El cliente solo puede cancelar un pedido mientras este se encuentre en estado *Recibido* o *En preparación*.
- Si el pedido ya está en estado *En camino*, la opción de cancelación debe estar deshabilitada.
- Al cancelar, el sistema solicita al cliente una razón de cancelación (campo opcional).
- El comercio y el repartidor (si ya fue asignado) reciben una notificación inmediata de la cancelación.
- El cliente recibe una confirmación de que la cancelación fue procesada exitosamente.
