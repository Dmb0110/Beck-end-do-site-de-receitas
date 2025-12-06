from fastapi import Request
from sqlalchemy.orm import Session
from app.models.models_receita import Receita
from app.schemas.schemas import CriarReceita, ReceitaOut
#import request

class ReceitaService:

    @staticmethod
    def criar_receita_auth(
        criar: CriarReceita,
        db: Session,
        imagem_url: str | None = None
) -> ReceitaOut:
        nova_receita = Receita(
            nome_da_receita=criar.nome_da_receita,
            ingredientes=criar.ingredientes,
            modo_de_preparo=criar.modo_de_preparo,
            imagem_url=imagem_url
        )
        db.add(nova_receita)
        db.commit()
        db.refresh(nova_receita)
        return nova_receita    
    