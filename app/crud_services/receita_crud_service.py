from fastapi import status, APIRouter, HTTPException, Depends, FastAPI
from sqlalchemy.orm import Session
from app.models.models_receita import Receita
from app.schemas.schemas import (
    CriarReceita, ReceitaOut, Atualizar, Deletar
)
from app.database.session import get_db
from typing import List

router = APIRouter()

class ReceitaService:
    """
    Camada de serviço responsável pelas operações CRUD relacionadas ao Cliente.
    Usa SQLAlchemy para persistência e schemas Pydantic para entrada/saída.
    """

    def __init__(self, db: Session = Depends(get_db)):
        # Injeta a sessão do banco via FastAPI Depends
        self.db = db


    def receber_todos_as_receitas(self) -> List[ReceitaOut]:
        """
        Retorna todos os clientes cadastrados.
        """
        receitas = self.db.query(Receita).all()
        return [ReceitaOut.from_orm(r) for r in receitas]
        #return [ReceitaOut.model_validate(c) for c in receitas]
    

    def trocar_receita(self, receita_id: int, at: Atualizar) -> ReceitaOut:
        """
        Atualiza dados de um cliente existente.
        - `cliente_id`: identificador do cliente.
        - `at`: schema com campos opcionais para atualização.
        """
        receita = self.db.query(Receita).filter(Receita.id == receita_id).first()
        if not receita:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        if at.nome_da_receita is not None:
            receita.nome_da_receita = at.nome_da_receita
        if at.ingredientes is not None:
            receita.ingredientes = at.ingredientes
        if at.modo_de_preparo is not None:
            receita.modo_de_preparo = at.modo_de_preparo

        self.db.commit()
        self.db.refresh(receita)
        return receita


    def deletar_receita(self, receita_id: int) -> dict:
        """
        Remove um cliente do banco.
        Retorna mensagem de sucesso ou lança 404 se não encontrado.
        """
        receita = self.db.query(Receita).filter(Receita.id == receita_id).first()
        if not receita:
            raise HTTPException(status_code=404, detail="Receita não encontrada")

        self.db.delete(receita)
        self.db.commit()
        return {"mensagem": "Receita deletada com sucesso"}


    def exibir_receita_especifica(self,id: int) -> ReceitaOut:
        receita = self.db.query(Receita).filter(Receita.id == id).first()
        if not receita:
            raise Exception('Receita nao encontrada')
        return ReceitaOut.from_orm(receita)
