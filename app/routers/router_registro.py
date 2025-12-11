from fastapi import APIRouter, Depends, status
from app.schemas.schemas import RegisterRequest
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.crud_services.registro_service import RegistroService

# Roteador para agrupar rotas de autenticação/registro
router = APIRouter()

@router.post(
    "/registro",
    summary="Rota para registrar usuário e senha",
    status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint responsável pelo registro de novos usuários.
    - Recebe dados validados pelo schema RegisterRequest.
    - Persiste o usuário no banco de dados via RegistroService.
    - Retorna o usuário criado ou lança exceção em caso de erro.

    Args:
        request (RegisterRequest): Dados de entrada (username, password).
        db (Session): Sessão do banco injetada via Depends.

    Returns:
        dict | UsuarioOut: Usuário registrado com sucesso.
    """
    return RegistroService.registrar_usuario(request, db)
