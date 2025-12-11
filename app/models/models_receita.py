from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

# ======================== Modelo da tabela 'receitas' ========================
class Receita(Base):
    """
    Representa a entidade Receita no banco de dados.
    - Utiliza SQLAlchemy ORM para mapear a tabela 'receitas'.
    - Cada instância corresponde a uma linha na tabela.
    """

    __tablename__ = 'receitas'

    # Identificador único da receita (chave primária).
    # 'index=True' facilita buscas por ID.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Nome da receita (até 100 caracteres).
    # 'nullable=False' garante que sempre haverá um nome.
    # 'index=True' permite buscas rápidas por nome.
    nome_da_receita: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Ingredientes da receita.
    # Usamos Text para permitir textos longos (listas de ingredientes).
    ingredientes: Mapped[str] = mapped_column(Text, nullable=False)

    # Modo de preparo da receita.
    # Também armazenado como Text para suportar instruções detalhadas.
    modo_de_preparo: Mapped[str] = mapped_column(Text, nullable=False)
