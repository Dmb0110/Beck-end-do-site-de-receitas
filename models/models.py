from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# URL de conexão com o banco de dados PostgreSQL
#DATABASE_URL = "postgresql://postgres:davi9090@db:5432/banco_dmb"

# Criação do engine e sessão para interagir com o banc
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

# Base para os modelos ORM
Base = declarative_base()

# Sobrescreve a URL do banco se estiver definida como variável de ambiente (útil para Docker)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Modelo da tabela 'usuarios'
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # pode ser o e-mail
    password = Column(String)

# Modelo da tabela 'receitas'
class Receita(Base):
    __tablename__ = 'receitas'

    id = Column(Integer,primary_key=True,index=True)
    nome_da_receita = Column(String)
    ingredientes = Column(String)
    modo_de_preparo = Column(String)
