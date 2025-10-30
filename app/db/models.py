from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DECIMAL,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from app.db.session import Base


# ========================
# 1️⃣ USUARIOS
# ========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # mesero, cocina, caja, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    comandas = relationship("Comanda", back_populates="mesero")


# ========================
# 2️⃣ MESAS
# ========================
class Mesa(Base):
    __tablename__ = "mesas"

    id_mesa = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    descripcion = Column(String(100))
    estado = Column(String(20), nullable=False)  # libre / ocupada
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    comandas = relationship("Comanda", back_populates="mesa")


# ========================
# 3️⃣ PRODUCTOS
# ========================
class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    categoria = Column(String(50))
    precio_vigente = Column(DECIMAL(10, 2), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    detalles = relationship("DetalleComanda", back_populates="producto")


# ========================
# 4️⃣ COMANDAS
# ========================
class Comanda(Base):
    __tablename__ = "comandas"

    id_comanda = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id_mesa", ondelete="SET NULL"))
    mesero_id = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"))
    estado = Column(String(20), nullable=False)  # hecho / entregado / finalizado
    es_para_llevar = Column(Boolean, default=False)
    notas = Column(Text)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")
    delivered_at = Column(TIMESTAMP)
    closed_at = Column(TIMESTAMP)

    mesa = relationship("Mesa", back_populates="comandas")
    mesero = relationship("Usuario", back_populates="comandas")
    comensales = relationship("Comensal", back_populates="comanda")
    detalles = relationship("DetalleComanda", back_populates="comanda")
    pago = relationship("Pago", back_populates="comanda", uselist=False)


# ========================
# 5️⃣ COMENSALES
# ========================
class Comensal(Base):
    __tablename__ = "comensales"

    id_comensal = Column(Integer, primary_key=True, index=True)
    comanda_id = Column(Integer, ForeignKey("comandas.id_comanda", ondelete="CASCADE"))
    nombre_alias = Column(String(100))
    grupo_cuenta = Column(String(50))
    created_at = Column(TIMESTAMP, server_default="now()")

    comanda = relationship("Comanda", back_populates="comensales")
    platos = relationship("Plato", back_populates="comensal")


# ========================
# 6️⃣ PLATOS
# ========================
class Plato(Base):
    __tablename__ = "platos"

    id_plato = Column(Integer, primary_key=True, index=True)
    comensal_id = Column(Integer, ForeignKey("comensales.id_comensal", ondelete="CASCADE"))
    nombre = Column(String(100))
    notas = Column(Text)
    created_at = Column(TIMESTAMP, server_default="now()")

    comensal = relationship("Comensal", back_populates="platos")
    detalles = relationship("DetalleComanda", back_populates="plato")


# ========================
# 7️⃣ DETALLE_COMANDA
# ========================
class DetalleComanda(Base):
    __tablename__ = "detalle_comanda"

    id_detalle = Column(Integer, primary_key=True, index=True)
    comanda_id = Column(Integer, ForeignKey("comandas.id_comanda", ondelete="CASCADE"))
    producto_id = Column(Integer, ForeignKey("productos.id_producto", ondelete="RESTRICT"))
    plato_id = Column(Integer, ForeignKey("platos.id_plato", ondelete="CASCADE"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    notas = Column(Text)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    comanda = relationship("Comanda", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")
    plato = relationship("Plato", back_populates="detalles")


# ========================
# 8️⃣ PAGOS
# ========================
class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    comanda_id = Column(Integer, ForeignKey("comandas.id_comanda", ondelete="CASCADE"), unique=True)
    metodo = Column(String(20), nullable=False)  # efectivo / tarjeta / transferencia
    total_pagado = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()")

    comanda = relationship("Comanda", back_populates="pago")
