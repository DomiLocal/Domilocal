from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

# --- Enums ---

class UserRole(str, Enum):
    CLIENTE = "cliente"
    VENDEDOR = "vendedor"
    REPARTIDOR = "repartidor"

class OrderStatus(str, Enum):
    RECIBIDO = "recibido"
    EN_PREPARACION = "en_preparacion"
    LISTO_PARA_RECOGER = "listo_para_recoger"
    EN_CAMINO = "en_camino"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class VehicleType(str, Enum):
    MOTO = "moto"
    BICI = "bici"
    CARRO = "carro"

class VendorStatus(str, Enum):
    PENDIENTE = "pendiente_aprobacion"
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class DeliveryStatus(str, Enum):
    PENDIENTE = "pendiente_activacion"
    DISPONIBLE = "disponible"
    NO_DISPONIBLE = "no_disponible"

# --- Models ---

class Product(BaseModel):
    id_producto: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    categoria: Optional[str] = None
    foto_url: Optional[str] = None
    disponible: bool = True

class Client(BaseModel):
    id_cliente: Optional[str] = None
    nombre: str
    correo: EmailStr
    telefono: str
    direccion_principal: str
    password: str = Field(..., min_length=8)
    rol: UserRole = UserRole.CLIENTE

class Vendor(BaseModel):
    id_comercio: Optional[str] = None
    nombre: str
    direccion: str
    categoria: str
    telefono: str
    correo: EmailStr
    estado: VendorStatus = VendorStatus.PENDIENTE
    productos: List[Product] = []

class DeliveryPerson(BaseModel):
    id_repartidor: Optional[str] = None
    nombre: str
    telefono: str
    correo: EmailStr
    password: str = Field(..., min_length=8)
    tipo_vehiculo: VehicleType
    nro_licencia: str
    estado: DeliveryStatus = DeliveryStatus.PENDIENTE

class OrderItem(BaseModel):
    nombre: str
    cantidad: int
    precio_unitario: float

class Order(BaseModel):
    id_pedido: Optional[str] = None
    id_cliente: str
    id_comercio: str
    productos: List[OrderItem]
    total: float
    estado: OrderStatus = OrderStatus.RECIBIDO
    metodo_pago: str
    direccion_entrega: str
    notas: Optional[str] = None
    id_repartidor: Optional[str] = None
    historial_estados: List[Dict[str, datetime]] = []
    fecha_creacion: datetime = Field(default_factory=datetime.now)
