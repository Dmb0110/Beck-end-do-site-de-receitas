from app.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

# ======================== Modelo da tabela 'usuarios' ========================
class Usuario(Base):
    """
    Representa a entidade Usuário no banco de dados.
    - Utiliza SQLAlchemy ORM para mapear a tabela 'usuarios'.
    - Cada instância corresponde a uma linha na tabela.
    """

    __tablename__ = 'usuarios'

    # Identificador único do usuário (chave primária).
    # 'index=True' facilita buscas rápidas por ID.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Nome de usuário (até 100 caracteres).
    # 'unique=True' garante que não haverá duplicidade.
    # Pode ser usado como e-mail para login.
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Senha do usuário (armazenada como hash).
    # Usamos String(255) para suportar hashes longos (ex.: bcrypt).
    # 'nullable=False' garante que sempre haverá senha registrada.
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        """Representação útil para debug/logs."""
        return f"<Usuario(id={self.id}, username={self.username})>"
