from fastapi import APIRouter, Depends, status, Request
from app.schemas.schemas import CriarReceita, ReceitaOut
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud_services.receita_auth_post_service import ReceitaService
from app.autenticacao10.jwt_auth2 import verificar_token, corrigir_texto
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

# Cria um roteador específico para rotas de receitas autenticadas
router = APIRouter()

# Middleware de segurança para extrair credenciais do header Authorization
security = HTTPBearer()

@router.post(
    '/enviar',
    summary='Rota protegida para criar receita',
    response_model=ReceitaOut,
    status_code=status.HTTP_201_CREATED
)
def enviar(
    criar: CriarReceita,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Endpoint protegido para criação de receitas.
    - Requer autenticação via token JWT (Bearer).
    - Recebe dados validados pelo schema CriarReceita.
    - Corrige texto (ortografia e capitalização) antes de salvar.
    - Persiste a receita no banco e retorna o objeto criado.

    Args:
        criar (CriarReceita): Dados da receita enviados pelo cliente.
        db (Session): Sessão do banco injetada via Depends.
        credentials (HTTPAuthorizationCredentials): Token JWT extraído do header Authorization.

    Returns:
        ReceitaOut: Receita criada e persistida no banco.
    """

    # Valida o token JWT e obtém o username associado
    username = verificar_token(credentials)

    # Corrige texto dos campos antes de salvar
    criar.nome_da_receita = corrigir_texto(criar.nome_da_receita)
    criar.ingredientes = corrigir_texto(criar.ingredientes)
    criar.modo_de_preparo = corrigir_texto(criar.modo_de_preparo)

    # Chama o serviço responsável por persistir a receita
    return ReceitaService.criar_receita_auth(criar, db)
