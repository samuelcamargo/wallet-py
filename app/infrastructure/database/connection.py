from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Alterando para SQLite
DATABASE_URL = "sqlite:///./wallet.db"

# Adicionando check_same_thread=False para permitir múltiplas threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 