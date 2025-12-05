from fastapi import HTTPException
from app.autenticacao10.jwt_auth2 import authenticate_user, create_token
from app.schemas.schemas import LoginRequest

class LoginService:

    @staticmethod
    def login(request: LoginRequest,db):    
        username = request.username
        password = request.password

        user = authenticate_user(db, username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        token = create_token({"sub": username})
        return {"access_token": token}
    