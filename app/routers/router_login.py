from fastapi import APIRouter, Depends, status
from app.schemas.schemas import LoginRequest
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud_services.login_service import LoginService

# Cria um roteador para agrupar rotas relacionadas à autenticação
router = APIRouter()

@router.post(
    "/login",
    summary="Cria login para o usuário e gera token JWT",
    status_code=status.HTTP_201_CREATED
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint responsável pelo login de usuários.
    - Recebe credenciais validadas pelo schema LoginRequest.
    - Consulta o banco de dados para autenticar o usuário.
    - Se válido, gera e retorna um token JWT.
    - Se inválido, lança HTTPException 401 (tratado dentro do LoginService).

    Args:
        request (LoginRequest): Dados de login (username e password).
        db (Session): Sessão do banco injetada via Depends.

    Returns:
        dict: Dicionário contendo o access_token JWT.
    """
    return LoginService.login(request, db)
