from fastapi import HTTPException
from app.autenticacao10.jwt_auth2 import authenticate_user, create_token
from app.schemas.schemas import LoginRequest

class LoginService:
    """
    Serviço responsável pela lógica de login de usuários.
    Centraliza autenticação e geração de token JWT.
    """

    @staticmethod
    def login(request: LoginRequest, db):
        """
        Realiza o processo de login:
        - Recebe um objeto LoginRequest (username e password).
        - Consulta o banco para verificar se o usuário existe e se a senha está correta.
        - Caso inválido, lança HTTPException 401.
        - Caso válido, gera e retorna um token JWT.
        
        Args:
            request (LoginRequest): Dados de login enviados pelo cliente.
            db (Session): Sessão do banco de dados para consulta.

        Returns:
            dict: Dicionário contendo o access_token JWT.
        """

        # Extrai credenciais do request
        username = request.username
        password = request.password

        # Autentica usuário no banco
        user = authenticate_user(db, username, password)
        if not user:
            # Retorna erro 401 se credenciais inválidas
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # Gera token JWT com o username como 'sub' (subject)
        token = create_token({"sub": username})

        # Retorna token para o cliente
        return {"access_token": token}
