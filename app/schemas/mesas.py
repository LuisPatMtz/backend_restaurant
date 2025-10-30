from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MesaBase(BaseModel):
    numero: int
    descripcion: Optional[str] = None


class MesaCreate(MesaBase):
    pass


class MesaUpdate(BaseModel):
    estado: Optional[str] = None
    descripcion: Optional[str] = None


class MesaResponse(MesaBase):
    id_mesa: int
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
