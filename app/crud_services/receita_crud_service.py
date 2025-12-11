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
    Camada de serviço responsável pelas operações CRUD relacionadas à entidade Receita.
    - Utiliza SQLAlchemy para persistência no banco de dados.
    - Usa schemas Pydantic para validação e serialização de entrada/saída.
    """

    def __init__(self, db: Session = Depends(get_db)):
        # Injeta a sessão do banco via FastAPI Depends
        self.db = db

    def receber_todos_as_receitas(self) -> List[ReceitaOut]:
        """
        Retorna todas as receitas cadastradas no banco.
        - Consulta todas as instâncias de Receita.
        - Converte cada objeto SQLAlchemy em um schema Pydantic (ReceitaOut).
        """
        receitas = self.db.query(Receita).all()
        return [ReceitaOut.from_orm(r) for r in receitas]
        # Alternativa: ReceitaOut.model_validate(c) para validação explícita

    def trocar_receita(self, receita_id: int, at: Atualizar) -> ReceitaOut:
        """
        Atualiza dados de uma receita existente.
        - `receita_id`: identificador da receita a ser atualizada.
        - `at`: schema com campos opcionais para atualização parcial.
        - Lança 404 se a receita não for encontrada.
        """
        receita = self.db.query(Receita).filter(Receita.id == receita_id).first()
        if not receita:
            raise HTTPException(status_code=404, detail="Receita não encontrada")

        # Atualiza apenas os campos fornecidos
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
        Remove uma receita do banco.
        - `receita_id`: identificador da receita a ser deletada.
        - Retorna mensagem de sucesso ou lança 404 se não encontrada.
        """
        receita = self.db.query(Receita).filter(Receita.id == receita_id).first()
        if not receita:
            raise HTTPException(status_code=404, detail="Receita não encontrada")

        self.db.delete(receita)
        self.db.commit()
        return {"mensagem": "Receita deletada com sucesso"}

    def exibir_receita_especifica(self, id: int) -> ReceitaOut:
        """
        Retorna uma receita específica pelo ID.
        - Lança exceção se não encontrada.
        """
        receita = self.db.query(Receita).filter(Receita.id == id).first()
        if not receita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Receita não encontrada'
            )
        return ReceitaOut.from_orm(receita)
