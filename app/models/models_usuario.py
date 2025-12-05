from app.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


# Modelo da tabela 'usuarios'
class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # pode ser o e-mail
    password: Mapped[str] = mapped_column(String(255),nullable=False)
