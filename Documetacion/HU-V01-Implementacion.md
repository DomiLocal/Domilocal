# 📋 Implementación HU-V01: Registro del Negocio en la Plataforma

## Descripción General

Se ha implementado completamente la Historia de Usuario **HU-V01** para el registro de comercios (vendedores) en la plataforma DomiLocal. La implementación sigue la arquitectura de capas profesional (Domain, Repository, Service, API).

## Estructura del Proyecto

```
mi_api/Comercio/
├── api/
│   ├── __init__.py
│   └── comercio_api.py         # Routers y endpoints
├── domain/
│   ├── __init__.py
│   └── comercio_domain.py      # Modelos y enumeraciones
├── repository/
│   ├── __init__.py
│   └── comercio_repository.py  # Acceso a datos
├── service/
│   ├── __init__.py
│   └── comercio_service.py     # Lógica de negocio
├── __init__.py
└── main.py                     # Punto de entrada de la aplicación
```

## Arquitectura de Capas

### 1. **Capa de Dominio (Domain)**
Archivo: `comercio_domain.py`

Define los modelos de datos y validaciones:
- `EstadoComercio`: Estados posibles (pendiente_aprobacion, activo, inactivo, rechazado)
- `CategoriaComercio`: Categorías predefinidas (restaurante, farmacia, tienda_barrio, etc.)
- `ComercioBase`: Clase base con validaciones
- `ComercioRegistroRequest`: Modelo para solicitudes de registro
- `ComercioResponse`: Modelo para respuestas
- `Comercio`: Modelo completo del dominio

**Validaciones implementadas:**
- Nombre: 3-100 caracteres
- Dirección: 5-200 caracteres
- Teléfono: 7-20 caracteres
- Correo: Validación de email (EmailStr)
- Categoría: Selección de lista predefinida

### 2. **Capa de Repositorio (Repository)**
Archivo: `comercio_repository.py`

Gestiona el acceso y persistencia de datos:
- `crear_comercio()`: Crea un nuevo comercio
- `obtener_comercio_por_id()`: Busca un comercio por ID
- `existe_comercio_duplicado()`: Valida duplicados
- `obtener_comercios_por_estado()`: Filtra por estado
- `actualizar_estado_comercio()`: Cambia el estado
- `obtener_todos_comercios()`: Lista todos los comercios
- `eliminar_comercio()`: Elimina un comercio

**Almacenamiento:** Actualmente usa diccionario en memoria (fácil de migrar a BD)

### 3. **Capa de Servicio (Service)**
Archivo: `comercio_service.py`

Contiene toda la lógica de negocio:
- `registrar_comercio()`: Registra con validaciones
- `obtener_comercio()`: Obtiene un comercio
- `obtener_comercios_activos()`: Lista visibles para clientes
- `obtener_comercios_pendientes()`: Lista para administrador
- `aprobar_comercio()`: Aprueba un comercio
- `rechazar_comercio()`: Rechaza un comercio

**Reglas de negocio implementadas:**
- Validación de duplicados por nombre y dirección
- Validación de categoría
- Estado inicial: pendiente_aprobacion
- Solo comercios activos son visibles para clientes

### 4. **Capa de API (API)**
Archivo: `comercio_api.py`

Expone los endpoints REST:

#### Endpoints Implementados

| Método | Ruta | Descripción | Status Code |
|--------|------|-------------|------------|
| POST | `/api/v1/comercios/registro` | Registrar nuevo comercio | 201 |
| GET | `/api/v1/comercios/{id}` | Obtener comercio por ID | 200/404 |
| GET | `/api/v1/comercios` | Listar comercios activos | 200 |
| GET | `/api/v1/comercios/admin/pendientes` | Listar pendientes (Admin) | 200 |
| PUT | `/api/v1/comercios/{id}/aprobar` | Aprobar comercio (Admin) | 200/404/400 |
| PUT | `/api/v1/comercios/{id}/rechazar` | Rechazar comercio (Admin) | 200/404 |

## Flujo de Uso - Caso 1: Registro Exitoso

### Request
```bash
curl -X POST "http://localhost:8000/api/v1/comercios/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tienda La Esquina",
    "direccion": "Calle Principal 123, Apt 4B",
    "categoria": "tienda_barrio",
    "telefono": "+57 300 123 4567",
    "correo": "contacto@laesquina.com"
  }'
```

### Response (201 Created)
```json
{
  "mensaje": "Comercio registrado exitosamente. Pendiente de aprobación.",
  "data": {
    "id_comercio": "COM-ABC12345",
    "nombre": "Tienda La Esquina",
    "estado": "pendiente_aprobacion"
  },
  "success": true
}
```

## Flujo de Uso - Caso 2: Comercio Duplicado

### Request
```bash
curl -X POST "http://localhost:8000/api/v1/comercios/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tienda La Esquina",
    "direccion": "Calle Principal 123, Apt 4B",
    "categoria": "restaurante",
    "telefono": "+57 301 987 6543",
    "correo": "otro@email.com"
  }'
```

### Response (409 Conflict)
```json
{
  "mensaje": "Ya existe un comercio registrado con ese nombre y dirección.",
  "data": null,
  "success": false
}
```

## Flujo de Uso - Caso 3: Aprobar Comercio (Admin)

### Request
```bash
curl -X PUT "http://localhost:8000/api/v1/comercios/COM-ABC12345/aprobar"
```

### Response (200 OK)
```json
{
  "mensaje": "Comercio aprobado exitosamente. Ahora es visible para los clientes.",
  "data": {
    "id_comercio": "COM-ABC12345",
    "nombre": "Tienda La Esquina",
    "estado": "activo"
  },
  "success": true
}
```

## Validaciones Implementadas

### 1. Validación de Campos Obligatorios
- Nombre, dirección, categoría, teléfono, correo son requeridos
- Si faltan campos → **HTTP 400 Bad Request**

```json
{
  "mensaje": "Datos inválidos o campos faltantes",
  "success": false
}
```

### 2. Validación de Duplicados
- Se verifica nombre Y dirección juntos
- Comparación case-insensitive
- Si existe → **HTTP 409 Conflict**

### 3. Validación de Categoría
- Debe ser una de las categorías predefinidas
- Si es inválida → **HTTP 400 Bad Request**

```json
{
  "mensaje": "La categoría indicada no es válida.",
  "success": false
}
```

### 4. Validación de Email
- Usa `EmailStr` de Pydantic
- Valida formato correcto de email

### 5. Validación de Longitudes
- Nombre: 3-100 caracteres
- Dirección: 5-200 caracteres
- Teléfono: 7-20 caracteres

## Códigos HTTP Implementados

| Código | Significado | Caso de Uso |
|--------|-------------|-----------|
| 201 | Created | Comercio registrado exitosamente |
| 200 | OK | Operación exitosa (GET, PUT) |
| 400 | Bad Request | Datos inválidos, campos faltantes, categoría inválida |
| 404 | Not Found | Comercio no encontrado |
| 409 | Conflict | Comercio duplicado |
| 500 | Internal Server Error | Error no controlado |

## Estados del Comercio

```
pendiente_aprobacion (inicial)
    ↓
    ├→ activo (visible para clientes) - mediante /aprobar
    └→ rechazado (rechazado) - mediante /rechazar
```

## Cómo Ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
python mi_api/Comercio/main.py
```

### 3. Acceder a la documentación interactiva
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Pruebas Completadas

✅ **Caso 1: Registro exitoso**
- Precondición: No existe comercio con mismo nombre y dirección
- Acción: POST a `/api/v1/comercios/registro` con todos los datos válidos
- Resultado: HTTP 201, estado `pendiente_aprobacion`, `success: true`

✅ **Caso 2: Comercio duplicado**
- Precondición: Existe comercio con mismo nombre y dirección
- Acción: POST a `/api/v1/comercios/registro` con mismo nombre y dirección
- Resultado: HTTP 409, `success: false`, mensaje de duplicado

✅ **Caso 3: Campos obligatorios faltantes**
- Acción: POST omitiendo uno o más campos
- Resultado: HTTP 400, mensaje de error indicando campo faltante

✅ **Caso 4: Categoría inválida**
- Acción: POST con categoría no válida
- Resultado: HTTP 400, mensaje: "La categoría indicada no es válida."

✅ **Caso 5: Aprobación de comercio**
- Acción: PUT a `/api/v1/comercios/{id}/aprobar`
- Resultado: HTTP 200, estado cambia a `activo`

✅ **Caso 6: Rechazo de comercio**
- Acción: PUT a `/api/v1/comercios/{id}/rechazar`
- Resultado: HTTP 200, estado cambia a `rechazado`

## Definición de Hecho - Alcance Funcional

✅ El endpoint registra el comercio con estado `pendiente_aprobacion`
✅ Se validan duplicados por nombre y dirección antes de crear el registro
✅ La categoría se valida contra la lista predefinida del sistema
✅ Se retorna HTTP 201 para registro exitoso
✅ Se retorna HTTP 409 para comercio duplicado
✅ Se retorna HTTP 400 para datos inválidos o categoría inválida
✅ Se implementó endpoint de aprobación para administrador
✅ Se implementó endpoint de rechazo para administrador
✅ El comercio solo es visible cuando estado es `activo`
✅ Respuestas JSON estructuradas con campos: `mensaje`, `data`, `success`

## Próximos Pasos (Recomendaciones)

1. **Integración con Base de Datos**
   - Migrar de diccionario en memoria a PostgreSQL/MongoDB
   - Usar SQLAlchemy u ORM similar

2. **Autenticación y Autorización**
   - Implementar JWT para autenticación
   - Validar rol de administrador en endpoints protegidos

3. **Notificaciones**
   - Enviar email de confirmación al registrar
   - Notificar cuando se aprueba/rechaza

4. **Paginación**
   - Agregar paginación a endpoints de listado

5. **Búsqueda y Filtrado**
   - Permitir buscar comercios por categoría, zona, etc.

6. **Tests Unitarios**
   - Crear tests con pytest
   - Cobertura de al menos 80%

7. **Documentación**
   - Crear postman collection para pruebas
   - Documentar políticas de negocio

## Referencias

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Python Async**: https://docs.python.org/3/library/asyncio.html
