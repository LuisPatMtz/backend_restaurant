from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.db import models
from app.schemas.comandas import ComandaCreate, ComandaResponse

router = APIRouter(prefix="/comandas", tags=["Comandas"])


# ======================================================
# 🧾 POST - Crear nueva comanda con sus detalles
# ======================================================
@router.post("/", response_model=ComandaResponse)
def crear_comanda(data: ComandaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva comanda (pedido) con sus detalles.
    Incluye validaciones de negocio:
    - La mesa no puede tener otra comanda activa.
    - Cambia el estado de la mesa a 'ocupada'.
    """
    try:
        # Validar mesa (si no es para llevar)
        if data.mesa_id:
            mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == data.mesa_id).first()
            if not mesa:
                raise HTTPException(status_code=404, detail="Mesa no encontrada")
            if mesa.estado != "libre":
                raise HTTPException(status_code=400, detail="La mesa está ocupada")

        # Crear comanda
        nueva_comanda = models.Comanda(
            mesa_id=data.mesa_id,
            mesero_id=data.mesero_id,
            estado="hecho",
            es_para_llevar=data.es_para_llevar,
            notas=data.notas,
            created_at=datetime.utcnow(),
        )
        db.add(nueva_comanda)
        db.flush()  # Obtener id_comanda antes del commit

        # Crear los detalles asociados
        for detalle in data.detalles:
            nuevo_detalle = models.DetalleComanda(
                comanda_id=nueva_comanda.id_comanda,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                notas=detalle.notas,
            )
            db.add(nuevo_detalle)

        # Cambiar estado de la mesa
        if data.mesa_id:
            mesa.estado = "ocupada"

        db.commit()
        db.refresh(nueva_comanda)

        # Recargar detalles desde la base
        nueva_comanda.detalles = (
            db.query(models.DetalleComanda)
            .filter(models.DetalleComanda.comanda_id == nueva_comanda.id_comanda)
            .all()
        )

        return nueva_comanda

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear comanda: {str(e)}")


# ======================================================
# 📋 GET - Listar todas las comandas con sus detalles
# ======================================================
@router.get("/", response_model=list[ComandaResponse])
def listar_comandas(db: Session = Depends(get_db)):
    """
    Listar todas las comandas registradas (con sus detalles).
    """
    comandas = db.query(models.Comanda).all()
    for comanda in comandas:
        comanda.detalles = (
            db.query(models.DetalleComanda)
            .filter(models.DetalleComanda.comanda_id == comanda.id_comanda)
            .all()
        )
    return comandas


# ======================================================
# 🔄 PATCH - Cambiar estado de una comanda
# ======================================================
@router.patch("/{comanda_id}/estado")
def cambiar_estado(
    comanda_id: int,
    nuevo_estado: str = Query(..., description="Estado: hecho | entregado | finalizado"),
    db: Session = Depends(get_db),
):
    """
    Actualizar el estado de una comanda:
    - hecho → entregado → finalizado
    Al finalizar, libera la mesa.
    """
    comanda = db.query(models.Comanda).filter(models.Comanda.id_comanda == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda no encontrada")

    # Validaciones
    if nuevo_estado not in ["hecho", "entregado", "finalizado"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    # Actualizar estado y timestamp
    comanda.estado = nuevo_estado
    comanda.updated_at = datetime.utcnow()

    # Si finaliza, liberar la mesa
    if nuevo_estado == "finalizado" and comanda.mesa_id:
        mesa = db.query(models.Mesa).filter(models.Mesa.id_mesa == comanda.mesa_id).first()
        if mesa:
            mesa.estado = "libre"

    db.commit()

    return {"message": f"Estado actualizado a '{nuevo_estado}' correctamente"}
