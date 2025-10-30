from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:ola990PATO..@localhost:5433/chechen_db"

# 👇  añadimos client_encoding y client_min_messages en UTF-8 y silenciamos advertencias
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c client_encoding=utf8 -c client_min_messages=warning",
    },
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
