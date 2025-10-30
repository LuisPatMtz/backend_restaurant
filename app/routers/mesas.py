from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.db import models
from app.schemas.mesas import MesaCreate, MesaResponse, MesaUpdate

router = APIRouter(prefix="/mesas", tags=["Mesas"])


# ======================================================
# ➕ POST - Registrar nueva mesa
# ======================================================
@router.post("/", response_model=MesaResponse)
def crear_mesa(data: MesaCreate, db: Session = Depends(get_db)):
    """
    Registrar una nueva mesa en el sistema.
    El número de mesa debe ser único.
    """
    existe = db.query(models.Mesa).filter(models.Mesa.numero == data.numero).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"La mesa número {data.numero} ya existe.")

    nueva_mesa = models.Mesa(
        numero=data.numero,
        descripcion=data.descripcion,
        estado="libre",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa


# ======================================================
# 📋 GET - Listar todas las mesas
# ======================================================
@router.get("/", response_model=list[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    """
    Listar todas las mesas con su estado actual.
    """
    mesas = db.query(models.Mesa).order_by(models.Mesa.numero).all()
    return mesas


# ======================================================
# 🔄 PATCH - Cambiar el estado de una mesa
# ======================================================
@router.patch("/{mesa_id}", response_model=MesaResponse)
def cambiar_estado_mesa(mesa_id: int, data: MesaUpdate, db: Session = Depends(get_db)):
    """
    Actualizar el estado o la descripción de una mesa.
    """
    mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")

    if data.estado and data.estado not in ["libre", "ocupada"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    if data.estado:
        mesa.estado = data.estado
    if data.descripcion is not None:
        mesa.descripcion = data.descripcion

    mesa.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(mesa)
    return mesa
