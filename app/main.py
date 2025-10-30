from fastapi import FastAPI
from app.db.session import engine, Base
from app.db import models

# Crear las tablas si no existen (solo la primera vez)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente 🚀"}

from app.routers import comandas
from app.routers import mesas
from app.routers import productos

app.include_router(comandas.router)
app.include_router(mesas.router)
app.include_router(productos.router)
