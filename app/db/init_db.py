from app.db.session import Base, engine
from app.db import models

print("🔄 Creando todas las tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")
