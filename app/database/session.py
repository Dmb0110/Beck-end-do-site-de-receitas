from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Cria a engine de conexão com o banco de dados usando a URL definida nas configurações
engine = create_engine(settings.DATABASE_URL)

# Cria uma fábrica de sessões (SessionLocal) para interagir com o banco
# autocommit=False → exige commit manual
# autoflush=False → evita flush automático antes de queries
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base declarativa usada para definir os modelos ORM
Base = declarative_base()

def get_db():
    """
    Dependência do FastAPI para obter uma sessão de banco.
    - Abre uma sessão (db).
    - Garante fechamento após uso (finally).
    - Usada com Depends(get_db) nas rotas/serviços.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
