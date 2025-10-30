from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio_vigente: float


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio_vigente: Optional[float] = None


class ProductoResponse(ProductoBase):
    id_producto: int
    activo: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
