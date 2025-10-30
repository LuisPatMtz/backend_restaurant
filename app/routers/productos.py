from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.db import models
from app.schemas.productos import ProductoCreate, ProductoResponse, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


# ======================================================
# ➕ POST - Registrar nuevo producto
# ======================================================
@router.post("/", response_model=ProductoResponse)
def crear_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo producto en el catálogo (platillo, bebida, etc.)
    """
    existe = db.query(models.Producto).filter(models.Producto.nombre == data.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre.")

    nuevo_producto = models.Producto(
        nombre=data.nombre,
        descripcion=data.descripcion,
        categoria=data.categoria,
        precio_vigente=data.precio_vigente,
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


# ======================================================
# 📋 GET - Listar todos los productos activos
# ======================================================
@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    """
    Obtener todos los productos activos.
    """
    productos = (
        db.query(models.Producto)
        .filter(models.Producto.activo == True)
        .order_by(models.Producto.nombre.asc())
        .all()
    )
    return productos


# ======================================================
# 🔄 PATCH - Actualizar datos de un producto
# ======================================================
@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    """
    Actualizar nombre, descripción, categoría o precio del producto.
    """
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if data.nombre:
        producto.nombre = data.nombre
    if data.descripcion is not None:
        producto.descripcion = data.descripcion
    if data.categoria is not None:
        producto.categoria = data.categoria
    if data.precio_vigente is not None:
        producto.precio_vigente = data.precio_vigente

    producto.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(producto)
    return producto


# ======================================================
# 🚫 DELETE lógico - Desactivar un producto
# ======================================================
@router.delete("/{producto_id}")
def desactivar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Desactiva un producto (borrado lógico).
    No se elimina físicamente por seguridad de auditoría.
    """
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.activo = False
    producto.updated_at = datetime.utcnow()
    db.commit()
    return {"message": f"Producto '{producto.nombre}' desactivado correctamente."}
