from fastapi import APIRouter, Depends, status
from app.schemas.schemas import LoginRequest
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud_services.login_service import LoginService

router = APIRouter()

@router.post(
        "/login",
        summary='Criar login para o usuario e gera token',
        status_code=status.HTTP_201_CREATED
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return LoginService.login(request,db)
