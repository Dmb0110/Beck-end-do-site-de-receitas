from fastapi import APIRouter, Depends, status
from app.schemas.schemas import RegisterRequest
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.crud_services.registro_service import RegistroService

router = APIRouter()

@router.post(
        "/",
        summary='Rota pra registrar usuario e senha',
        status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    return RegistroService.registrar_usuario(request,db)
