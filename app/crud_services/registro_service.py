from fastapi import HTTPException
from app.models.models_usuario import Usuario
from app.schemas.schemas import RegisterRequest
from sqlalchemy.orm import Session
from app.autenticacao10.jwt_auth2 import pwd_context

class RegistroService:

    @staticmethod
    def registrar_usuario(request: RegisterRequest,db: Session) -> dict:
        existing_user = db.query(Usuario).filter(Usuario.username == request.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Usuário já existe")

        hashed_password = pwd_context.hash(request.password)

        novo_usuario = Usuario(username=request.username, password=hashed_password)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {"mensagem": "Usuário registrado com sucesso"}
