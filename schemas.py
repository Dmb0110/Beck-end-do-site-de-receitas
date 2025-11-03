from typing import Optional
from pydantic import BaseModel

# Modelo para requisição de login
class LoginRequest(BaseModel):
    username: str
    password: str

# Modelo para requisição de registro de usuário
class RegisterRequest(BaseModel):
    username: str
    password: str

# Modelo para criação de uma nova receita
class CriarReceita(BaseModel):
    nome_da_receita: str
    ingredientes: str
    modo_de_preparo: str

# Modelo de saída de receita (inclui ID)
class ReceitaOut(BaseModel):
    id: int
    nome_da_receita: str
    ingredientes: str
    modo_de_preparo: str

    class Config:
        from_attributes = True # Permite conversão direta de ORM para Pydantic

# Modelo para atualização parcial de receita
class Atualizar(BaseModel):
    nome_da_receita: Optional[str] = None
    ingredientes: Optional[str] = None
    modo_de_preparo: Optional[str] = None

# Modelo para resposta de exclusão
class Deletar(BaseModel):
    mensagem: bool
