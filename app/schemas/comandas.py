from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DetalleComandaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    notas: Optional[str] = None


class DetalleComandaResponse(DetalleComandaBase):
    id_detalle: int
    created_at: datetime

    class Config:
        orm_mode = True


class ComandaCreate(BaseModel):
    mesa_id: Optional[int]
    mesero_id: int
    es_para_llevar: bool = False
    notas: Optional[str] = None
    detalles: List[DetalleComandaBase]


class ComandaResponse(BaseModel):
    id_comanda: int
    mesa_id: Optional[int]
    mesero_id: int
    estado: str
    es_para_llevar: bool
    notas: Optional[str]
    created_at: datetime
    detalles: List[DetalleComandaResponse] = []

    class Config:
        orm_mode = True
