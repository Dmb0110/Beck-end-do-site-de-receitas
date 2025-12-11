from fastapi import Request
from sqlalchemy.orm import Session
from app.models.models_receita import Receita
from app.schemas.schemas import CriarReceita, ReceitaOut

class ReceitaService:
    """
    Serviço responsável pela lógica de criação de receitas autenticadas.
    Encapsula a interação entre os schemas (entrada/saída) e o modelo SQLAlchemy.
    """

    @staticmethod
    def criar_receita_auth(
        criar: CriarReceita,
        db: Session,
    ) -> ReceitaOut:
        """
        Cria uma nova receita no banco de dados.

        Args:
            criar (CriarReceita): Schema Pydantic contendo os dados da receita.
            db (Session): Sessão ativa do SQLAlchemy para persistência.
            imagem_url (str | None): URL opcional de imagem da receita (não implementado).

        Returns:
            ReceitaOut: Objeto da receita criada, já persistido e atualizado.
        """

        # Instancia o modelo Receita com os dados recebidos
        nova_receita = Receita(
            nome_da_receita=criar.nome_da_receita,
            ingredientes=criar.ingredientes,
            modo_de_preparo=criar.modo_de_preparo,
            # imagem_url=imagem_url
        )

        # Adiciona a nova receita à sessão
        db.add(nova_receita)

        # Persiste a transação no banco
        db.commit()

        # Atualiza o objeto com os dados definitivos (ex.: id gerado)
        db.refresh(nova_receita)

        # Retorna a receita criada
        return nova_receita
