#from dotenv import load_dotenv
#from fastapi import FastAPI
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base
#import os

# Modelo da tabela 'receitas'
class Receita(Base):
    __tablename__ = 'receitas'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    nome_da_receita: Mapped[str] = mapped_column(String(100), nullable=False,index=True)
    ingredientes: Mapped[str] = mapped_column(Text, nullable=False)
    modo_de_preparo: Mapped[str] = mapped_column(Text, nullable=False)
    #imagem_url: Mapped[str] = mapped_column(String,nullable=True)
